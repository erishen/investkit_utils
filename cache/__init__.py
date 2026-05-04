"""InvestKit 缓存模块

提供统一的缓存抽象层，支持多种后端:
- Memory: 内存缓存 (默认)
- Redis: 分布式缓存

使用示例:
    from investkit_utils.cache import get_cache, cached

    # 获取缓存实例
    cache = get_cache()

    # 基本操作
    cache.set("key", "value", ttl=3600)
    value = cache.get("key")
    cache.delete("key")

    # 使用装饰器缓存函数结果
    @cached(ttl=300)
    def expensive_function(arg):
        return compute(arg)
"""

from investkit_utils.cache.base import CacheBackend
from investkit_utils.cache.memory import MemoryCache
from investkit_utils.cache.manager import (
    get_cache,
    get_memory_cache,
    get_redis_cache,
    clear_all_caches,
)
from investkit_utils.cache.decorators import (
    cached,
    cached_async,
    cache_result,
    invalidate_cache,
)

__all__ = [
    "CacheBackend",
    "MemoryCache",
    "get_cache",
    "get_memory_cache",
    "get_redis_cache",
    "clear_all_caches",
    "cached",
    "cached_async",
    "cache_result",
    "invalidate_cache",
]
