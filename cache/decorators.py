"""InvestKit 缓存装饰器

提供函数结果缓存装饰器。
"""

from __future__ import annotations

import functools
import hashlib
import inspect
from typing import Any, Callable, Optional, TypeVar, Union

from investkit_utils.cache.base import CacheBackend
from investkit_utils.cache.manager import get_cache

T = TypeVar("T")
F = Callable[..., T]


def _make_cache_key(
    func: Callable,
    args: tuple,
    kwargs: dict,
    key_prefix: Optional[str] = None,
) -> str:
    """生成缓存键

    Args:
        func: 函数
        args: 位置参数
        kwargs: 关键字参数
        key_prefix: 键前缀

    Returns:
        缓存键
    """
    parts = [func.__module__, func.__qualname__]

    if args:
        parts.append(str(args))
    if kwargs:
        parts.append(str(sorted(kwargs.items())))

    key_content = ":".join(parts)
    key_hash = hashlib.md5(key_content.encode()).hexdigest()[:12]

    if key_prefix:
        return f"{key_prefix}:{func.__name__}:{key_hash}"
    return f"cached:{func.__name__}:{key_hash}"


def cached(
    ttl: Optional[int] = None,
    key_prefix: Optional[str] = None,
    cache: Optional[Union[CacheBackend, str]] = None,
) -> Callable[[F], F]:
    """缓存装饰器 (同步函数)

    Args:
        ttl: 过期时间 (秒)
        key_prefix: 键前缀
        cache: 缓存实例或名称

    Returns:
        装饰器

    示例:
        @cached(ttl=300)
        def expensive_function(arg):
            return compute(arg)
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            cache_instance: CacheBackend
            if cache is None:
                cache_instance = get_cache()
            elif isinstance(cache, str):
                cache_instance = get_cache(cache)
            else:
                cache_instance = cache

            key = _make_cache_key(func, args, kwargs, key_prefix)

            cached_value = cache_instance.get(key)
            if cached_value is not None:
                return cached_value

            result = func(*args, **kwargs)
            cache_instance.set(key, result, ttl)

            return result

        wrapper._cache_info = {  # type: ignore
            "ttl": ttl,
            "key_prefix": key_prefix,
        }

        return wrapper  # type: ignore

    return decorator


def cached_async(
    ttl: Optional[int] = None,
    key_prefix: Optional[str] = None,
    cache: Optional[Union[CacheBackend, str]] = None,
) -> Callable[[F], F]:
    """缓存装饰器 (异步函数)

    Args:
        ttl: 过期时间 (秒)
        key_prefix: 键前缀
        cache: 缓存实例或名称

    Returns:
        装饰器

    示例:
        @cached_async(ttl=300)
        async def async_function(arg):
            return await compute(arg)
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            cache_instance: CacheBackend
            if cache is None:
                cache_instance = get_cache()
            elif isinstance(cache, str):
                cache_instance = get_cache(cache)
            else:
                cache_instance = cache

            key = _make_cache_key(func, args, kwargs, key_prefix)

            cached_value = cache_instance.get(key)
            if cached_value is not None:
                return cached_value

            result = await func(*args, **kwargs)
            cache_instance.set(key, result, ttl)

            return result

        wrapper._cache_info = {  # type: ignore
            "ttl": ttl,
            "key_prefix": key_prefix,
        }

        return wrapper  # type: ignore

    return decorator


def cache_result(
    func: Optional[F] = None,
    *,
    ttl: Optional[int] = None,
    key_prefix: Optional[str] = None,
) -> Union[F, Callable[[F], F]]:
    """智能缓存装饰器

    自动检测同步/异步函数并使用对应的装饰器。

    Args:
        func: 函数 (可选)
        ttl: 过期时间 (秒)
        key_prefix: 键前缀

    Returns:
        装饰器或装饰后的函数

    示例:
        @cache_result(ttl=300)
        def sync_func(arg):
            return compute(arg)

        @cache_result(ttl=300)
        async def async_func(arg):
            return await compute(arg)
    """

    def decorator(f: F) -> F:
        if inspect.iscoroutinefunction(f):
            return cached_async(ttl=ttl, key_prefix=key_prefix)(f)
        return cached(ttl=ttl, key_prefix=key_prefix)(f)

    if func is not None:
        return decorator(func)
    return decorator


def invalidate_cache(
    func: Callable,
    *args: Any,
    key_prefix: Optional[str] = None,
    cache: Optional[Union[CacheBackend, str]] = None,
    **kwargs: Any,
) -> bool:
    """使缓存失效

    Args:
        func: 函数
        *args: 位置参数
        key_prefix: 键前缀
        cache: 缓存实例或名称
        **kwargs: 关键字参数

    Returns:
        是否删除成功
    """
    cache_instance: CacheBackend
    if cache is None:
        cache_instance = get_cache()
    elif isinstance(cache, str):
        cache_instance = get_cache(cache)
    else:
        cache_instance = cache

    key = _make_cache_key(func, args, kwargs, key_prefix)
    return cache_instance.delete(key)
