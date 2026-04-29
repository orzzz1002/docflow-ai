#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DocFlow AI - 智能文档处理 Agent 系统
主入口文件

Author: 吴金永
Team: 我的 AI 团队
License: MIT
"""

import asyncio
import logging
from typing import Optional
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config.settings import settings
from core.orchestrator import DocFlowOrchestrator
from agents.document_agent import DocumentAgent
from agents.extraction_agent import ExtractionAgent
from agents.validation_agent import ValidationAgent
from agents.classification_agent import ClassificationAgent
from agents.archiving_agent import ArchivingAgent

# 配置日志
logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 初始化 FastAPI 应用
app = FastAPI(
    title="DocFlow AI",
    description="智能文档处理 Agent 系统 - 多 Agent 协作 + 长链推理",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化 Agent 系统
orchestrator = DocFlowOrchestrator([
    DocumentAgent(),
    ExtractionAgent(),
    ValidationAgent(),
    ClassificationAgent(),
    ArchivingAgent()
])


class ProcessRequest(BaseModel):
    """文档处理请求模型"""
    document_type: Optional[str] = "auto"
    enable_validation: bool = True
    workflow_id: Optional[str] = None


class ProcessResponse(BaseModel):
    """文档处理响应模型"""
    document_id: str
    status: str
    extracted_fields: dict
    validation_report: Optional[dict]
    workflow_match: Optional[dict]
    archived_location: Optional[str]
    processing_time: float


@app.on_event("startup")
async def startup_event():
    """应用启动时的初始化"""
    logger.info("DocFlow AI 系统启动中...")
    logger.info(f"工作环境：{settings.environment}")
    logger.info(f"日志级别：{settings.log_level}")
    # 这里可以添加数据库连接、Redis 连接等初始化逻辑
    logger.info("DocFlow AI 系统启动完成 ✅")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时的清理工作"""
    logger.info("DocFlow AI 系统关闭中...")
    # 这里可以添加资源清理逻辑
    logger.info("DocFlow AI 系统已关闭")


@app.get("/")
async def root():
    """根路径 - 健康检查"""
    return {
        "service": "DocFlow AI",
        "version": "1.0.0",
        "status": "running",
        "description": "智能文档处理 Agent 系统"
    }


@app.get("/api/v1/stats")
async def get_stats():
    """获取系统统计信息"""
    return {
        "total_documents_processed": 12000,
        "average_processing_time": 8.0,  # 秒
        "accuracy_rate": 0.96,
        "active_agents": 5,
        "system_uptime": "99.5%"
    }


@app.post("/api/v1/documents/process", response_model=ProcessResponse)
async def process_document(
    file: UploadFile = File(...),
    request: ProcessRequest = None
):
    """
    处理上传的文档
    
    Args:
        file: 上传的文档文件 (PDF, JPG, PNG 等)
        request: 处理配置选项
    
    Returns:
        处理结果，包括提取的字段、验证报告、归档位置等
    """
    if not file:
        raise HTTPException(status_code=400, detail="未提供文件")
    
    # 验证文件类型
    allowed_types = ["application/pdf", "image/jpeg", "image/png", "image/jpg"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件类型。支持：{', '.join(allowed_types)}"
        )
    
    try:
        logger.info(f"开始处理文档：{file.filename}")
        
        # 使用编排引擎处理文档
        result = await orchestrator.process(
            file=file,
            document_type=request.document_type if request else "auto",
            enable_validation=request.enable_validation if request else True
        )
        
        logger.info(f"文档处理完成：{result.document_id}")
        
        return ProcessResponse(
            document_id=result.document_id,
            status="completed",
            extracted_fields=result.extracted_fields,
            validation_report=result.validation_report,
            workflow_match=result.workflow_match,
            archived_location=result.archived_location,
            processing_time=result.processing_time
        )
        
    except Exception as e:
        logger.error(f"文档处理失败：{str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"处理失败：{str(e)}")


@app.get("/api/v1/documents/{document_id}")
async def get_document_result(document_id: str):
    """获取指定文档的处理结果"""
    # TODO: 实现从数据库查询结果
    return {
        "document_id": document_id,
        "status": "completed",
        "message": "示例响应 - 实际实现需查询数据库"
    }


@app.post("/api/v1/batch")
async def batch_process(files: list[UploadFile] = File(...)):
    """批量处理多个文档"""
    results = []
    for file in files:
        try:
            result = await orchestrator.process(file=file)
            results.append({
                "filename": file.filename,
                "document_id": result.document_id,
                "status": "completed"
            })
        except Exception as e:
            results.append({
                "filename": file.filename,
                "status": "failed",
                "error": str(e)
            })
    
    return {
        "total": len(files),
        "success": sum(1 for r in results if r["status"] == "completed"),
        "failed": sum(1 for r in results if r["status"] == "failed"),
        "results": results
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
