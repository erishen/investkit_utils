"""日志上下文管理"""

from contextvars import ContextVar
from typing import Optional


_correlation_id: ContextVar[Optional[str]] = ContextVar("correlation_id", default=None)


def set_correlation_id(cid: str) -> None:
    """设置当前请求的关联 ID"""
    _correlation_id.set(cid)


def get_correlation_id() -> Optional[str]:
    """获取当前请求的关联 ID"""
    return _correlation_id.get()
