#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统配置文件
"""

import os
from pydantic import BaseSettings
from typing import List


class Settings(BaseSettings):
    """系统配置"""
    
    # 基础配置
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    
    # 日志配置
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # CORS 配置
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "*"
    ]
    
    # 数据库配置
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/docflow"
    )
    
    # Redis 配置
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # AI 模型配置
    ai_model_path: str = os.getenv("AI_MODEL_PATH", "./models")
    max_document_size_mb: int = int(os.getenv("MAX_DOCUMENT_SIZE", "20"))
    
    # 安全配置
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    api_key_header: str = "X-API-Key"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# 全局配置实例
settings = Settings()
