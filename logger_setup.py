"""
日志系统配置
提供统一的日志配置和管理功能
"""

import logging
import logging.handlers
import os
import sys
from pathlib import Path
from typing import Optional


class LoggerSetup:
    """日志系统配置器"""
    
    @staticmethod
    def setup_logger(
        name: str = 'henu_login',
        level: str = 'INFO',
        log_file: Optional[str] = None,
        max_size_mb: int = 10,
        backup_count: int = 5,
        console_output: bool = True
    ) -> logging.Logger:
        """
        设置日志系统
        
        Args:
            name: 日志器名称
            level: 日志级别（DEBUG, INFO, WARNING, ERROR, CRITICAL）
            log_file: 日志文件路径
            max_size_mb: 日志文件最大大小（MB）
            backup_count: 保留的日志文件备份数量
            console_output: 是否输出到控制台
            
        Returns:
            配置好的logger对象
        """
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper(), logging.INFO))
        
        # 清除已存在的处理器
        logger.handlers.clear()
        
        # 创建格式化器
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        simple_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        
        # 添加文件处理器（带日志轮转）
        if log_file:
            try:
                # 确保日志目录存在
                log_dir = os.path.dirname(log_file)
                if log_dir:
                    os.makedirs(log_dir, exist_ok=True)
                
                file_handler = logging.handlers.RotatingFileHandler(
                    log_file,
                    maxBytes=max_size_mb * 1024 * 1024,
                    backupCount=backup_count,
                    encoding='utf-8'
                )
                file_handler.setLevel(logging.DEBUG)
                file_handler.setFormatter(detailed_formatter)
                logger.addHandler(file_handler)
            except Exception as e:
                print(f"警告: 无法创建日志文件 {log_file}: {e}", file=sys.stderr)
        
        # 添加控制台处理器
        if console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(simple_formatter)
            logger.addHandler(console_handler)
        
        return logger
    
    @staticmethod
    def get_logger(name: str = 'henu_login') -> logging.Logger:
        """获取已配置的logger"""
        return logging.getLogger(name)
