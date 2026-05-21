"""日志管理器"""

import logging
import sys
from functools import lru_cache

from investkit_utils.log_utils.config import LogFormat, LoggingConfig
from investkit_utils.log_utils.formatters import JsonFormatter, TextFormatter
from investkit_utils.log_utils.logger import InvestKitLogger


class LoggerManager:
    """日志管理器"""

    _config: LoggingConfig = LoggingConfig()
    _initialized: bool = False

    @classmethod
    def configure(cls, config: LoggingConfig) -> None:
        """配置日志系统"""
        cls._config = config
        cls._initialized = True

        logging.setLoggerClass(InvestKitLogger)

        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, config.level.upper()))

        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        if config.console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(getattr(logging, config.level.upper()))

            if config.format == LogFormat.JSON:
                console_handler.setFormatter(
                    JsonFormatter(
                        include_module=config.include_module,
                        include_correlation_id=config.include_correlation_id,
                    )
                )
            else:
                console_handler.setFormatter(
                    TextFormatter(
                        include_module=config.include_module,
                        include_correlation_id=config.include_correlation_id,
                    )
                )

            root_logger.addHandler(console_handler)

        if config.file_output:
            import os
            from logging.handlers import RotatingFileHandler

            os.makedirs(os.path.dirname(config.file_path), exist_ok=True)

            file_handler = RotatingFileHandler(
                config.file_path,
                maxBytes=config.rotation_max_bytes,
                backupCount=config.rotation_backup_count,
                encoding="utf-8",
            )
            file_handler.setLevel(getattr(logging, config.level.upper()))

            if config.format == LogFormat.JSON:
                file_handler.setFormatter(
                    JsonFormatter(
                        include_module=config.include_module,
                        include_correlation_id=config.include_correlation_id,
                    )
                )
            else:
                file_handler.setFormatter(
                    TextFormatter(
                        include_module=config.include_module,
                        include_correlation_id=config.include_correlation_id,
                    )
                )

            root_logger.addHandler(file_handler)

    @classmethod
    def get_config(cls) -> LoggingConfig:
        """获取当前配置"""
        return cls._config


@lru_cache(maxsize=128)
def get_logger(name: str) -> InvestKitLogger:
    """
    获取 Logger 实例

    Args:
        name: 模块名称，通常使用 __name__

    Returns:
        InvestKitLogger 实例
    """
    if not LoggerManager._initialized:
        LoggerManager.configure(LoggingConfig())

    return logging.getLogger(name)


def setup_logging(
    level: str = "INFO",
    log_format: str = "json",
    console: bool = True,
    file_path: str | None = None,
    include_module: bool = True,
    include_correlation_id: bool = True,
) -> None:
    """
    快速设置日志

    Args:
        level: 日志级别
        log_format: 日志格式 (json/text)
        console: 是否输出到控制台
        file_path: 日志文件路径
        include_module: 是否包含模块信息
        include_correlation_id: 是否包含关联 ID
    """
    config = LoggingConfig(
        level=level,
        format=LogFormat(log_format),
        console_output=console,
        file_output=file_path is not None,
        file_path=file_path or "logs/app.log",
        include_module=include_module,
        include_correlation_id=include_correlation_id,
    )
    LoggerManager.configure(config)
