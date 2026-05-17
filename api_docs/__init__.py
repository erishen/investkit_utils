"""
InvestKit API 文档聚合模块

聚合各项目的 OpenAPI 文档，提供统一的 API 文档入口。

使用示例:
    from investkit_utils.api_docs import aggregate_openapi_docs, serve_aggregated_docs

    # 聚合文档
    app = serve_aggregated_docs()
"""

from investkit_utils.api_docs.discovery import (
    HealthCheckResult,
    ServiceInfo,
    ServiceRegistry,
    ServiceStatus,
    get_all_services,
    get_service,
    get_service_registry,
    register_service,
)
from investkit_utils.api_docs.openapi import (
    aggregate_from_files,
    aggregate_openapi_docs,
    clear_cache,
    fetch_openapi_spec,
    load_openapi_spec_from_file,
    merge_openapi_specs,
    set_cache,
)
from investkit_utils.api_docs.server import serve_aggregated_docs
from investkit_utils.api_docs.services import (
    INVESTKIT_SERVICES,
    APIService,
)

__all__ = [
    "INVESTKIT_SERVICES",
    "APIService",
    "HealthCheckResult",
    "ServiceInfo",
    "ServiceRegistry",
    "ServiceStatus",
    "aggregate_from_files",
    "aggregate_openapi_docs",
    "clear_cache",
    "fetch_openapi_spec",
    "get_all_services",
    "get_service",
    "get_service_registry",
    "load_openapi_spec_from_file",
    "merge_openapi_specs",
    "register_service",
    "serve_aggregated_docs",
    "set_cache",
]
