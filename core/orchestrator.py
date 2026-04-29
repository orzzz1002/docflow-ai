#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
编排引擎 - 协调多 Agent 协作的核心组件
"""

from typing import Any, Dict, List
import time
from agents.base_agent import BaseAgent, AgentResult


class DocFlowOrchestrator:
    """
    文档处理编排引擎
    
    职责：
    - 协调多个 Agent 按顺序或并行执行
    - 管理 Agent 之间的数据传递
    - 处理异常和回滚
    """
    
    def __init__(self, agents: List[BaseAgent]):
        self.agents = agents
        self.agent_map = {agent.name: agent for agent in agents}
    
    async def process(self, file: Any, document_type: str = "auto", 
                     enable_validation: bool = True) -> AgentResult:
        """
        编排完整的文档处理流程
        
        流程：
        1. Document Agent - 文档理解
        2. Extraction Agent - 信息抽取
        3. Validation Agent - 逻辑验证（可选）
        4. Classification Agent - 业务分类
        5. Archiving Agent - 归档
        """
        start_time = time.time()
        context = {"file": file, "document_type": document_type}
        
        try:
            # 步骤 1: 文档理解
            doc_result = await self.agent_map["DocumentAgent"].process(file)
            if not doc_result.success:
                raise Exception(f"文档分析失败：{doc_result.error}")
            context["document_analysis"] = doc_result.data
            
            # 步骤 2: 信息抽取
            ext_result = await self.agent_map["ExtractionAgent"].process(context)
            if not ext_result.success:
                raise Exception(f"信息抽取失败：{ext_result.error}")
            context["extracted_data"] = ext_result.data
            
            # 步骤 3: 逻辑验证（可选）
            if enable_validation:
                val_result = await self.agent_map["ValidationAgent"].process({
                    "extracted_data": context["extracted_data"]
                })
                context["validation_report"] = val_result.data
                if not val_result.is_valid:
                    context["validation_warnings"] = val_result.warnings
            
            # 步骤 4: 业务分类
            cls_result = await self.agent_map["ClassificationAgent"].process(context)
            if not cls_result.success:
                raise Exception(f"分类失败：{cls_result.error}")
            context["workflow"] = cls_result.data
            
            # 步骤 5: 归档
            arch_result = await self.agent_map["ArchivingAgent"].process(context)
            if not arch_result.success:
                raise Exception(f"归档失败：{arch_result.error}")
            
            processing_time = time.time() - start_time
            
            return AgentResult(
                success=True,
                data={
                    "document_id": f"doc_{int(time.time())}",
                    "processing_time": processing_time,
                    **context
                },
                metadata={
                    "agents_used": len(self.agents),
                    "validation_enabled": enable_validation
                }
            )
            
        except Exception as e:
            return AgentResult(
                success=False,
                error=str(e),
                processing_time=time.time() - start_time
            )
