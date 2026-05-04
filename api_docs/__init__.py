"""
InvestKit API 文档聚合模块

聚合各项目的 OpenAPI 文档，提供统一的 API 文档入口。

使用示例:
    from investkit_utils.api_docs import aggregate_openapi_docs, serve_aggregated_docs

    # 聚合文档
    app = serve_aggregated_docs()
"""

from investkit_utils.api_docs.services import (
    APIService,
    INVESTKIT_SERVICES,
)

from investkit_utils.api_docs.openapi import (
    merge_openapi_specs,
    fetch_openapi_spec,
    aggregate_openapi_docs,
    load_openapi_spec_from_file,
    aggregate_from_files,
    set_cache,
    clear_cache,
)

from investkit_utils.api_docs.discovery import (
    ServiceRegistry,
    ServiceInfo,
    ServiceStatus,
    HealthCheckResult,
    get_service_registry,
    register_service,
    get_service,
    get_all_services,
)

from investkit_utils.api_docs.server import serve_aggregated_docs


__all__ = [
    "APIService",
    "INVESTKIT_SERVICES",
    "merge_openapi_specs",
    "fetch_openapi_spec",
    "aggregate_openapi_docs",
    "load_openapi_spec_from_file",
    "aggregate_from_files",
    "set_cache",
    "clear_cache",
    "ServiceRegistry",
    "ServiceInfo",
    "ServiceStatus",
    "HealthCheckResult",
    "get_service_registry",
    "register_service",
    "get_service",
    "get_all_services",
    "serve_aggregated_docs",
]
