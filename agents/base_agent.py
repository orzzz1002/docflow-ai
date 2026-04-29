#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent 基类 - 所有 Agent 的抽象父类
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel
import time


class AgentResult(BaseModel):
    """Agent 执行结果基类"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    processing_time: float = 0.0
    metadata: Dict[str, Any] = {}


class BaseAgent(ABC):
    """
    Agent 基类
    
    所有专用 Agent 都应继承此类并实现其抽象方法
    """
    
    def __init__(self, name: str = "BaseAgent"):
        self.name = name
        self.initialized = False
    
    async def initialize(self) -> bool:
        """初始化 Agent（可选，用于加载模型、建立连接等）"""
        self.initialized = True
        return True
    
    @abstractmethod
    async def execute(self, input_data: Any) -> AgentResult:
        """
        执行 Agent 的核心逻辑
        
        Args:
            input_data: 输入数据
            
        Returns:
            AgentResult: 执行结果
        """
        pass
    
    async def process(self, input_data: Any) -> AgentResult:
        """
        处理输入的模板方法（包含计时和错误处理）
        
        Args:
            input_data: 输入数据
            
        Returns:
            AgentResult: 处理结果
        """
        start_time = time.time()
        
        try:
            if not self.initialized:
                await self.initialize()
            
            result = await self.execute(input_data)
            result.processing_time = time.time() - start_time
            result.success = True
            
            return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            return AgentResult(
                success=False,
                error=str(e),
                processing_time=processing_time
            )
    
    def get_status(self) -> Dict[str, Any]:
        """获取 Agent 状态"""
        return {
            "name": self.name,
            "initialized": self.initialized,
            "type": self.__class__.__name__
        }
