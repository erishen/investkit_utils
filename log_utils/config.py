"""日志配置"""

from dataclasses import dataclass
from enum import Enum


class LogFormat(Enum):
    JSON = "json"
    TEXT = "text"


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class LoggingConfig:
    """日志配置"""

    level: str = "INFO"
    format: LogFormat = LogFormat.JSON
    console_output: bool = True
    file_output: bool = False
    file_path: str = "logs/app.log"
    include_timestamp: bool = True
    include_module: bool = True
    include_correlation_id: bool = True
    rotation_max_bytes: int = 10 * 1024 * 1024
    rotation_backup_count: int = 5
