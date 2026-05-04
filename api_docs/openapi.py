"""OpenAPI 规范处理"""

import json
from pathlib import Path
from typing import Any, Optional, List

from investkit_utils.api_docs.services import APIService


def merge_openapi_specs(
    specs: List[dict],
    main_info: Optional[dict] = None,
) -> dict:
    """
    合并多个 OpenAPI 规范

    Args:
        specs: OpenAPI 规范列表
        main_info: 主信息 (可选)

    Returns:
        合并后的 OpenAPI 规范
    """
    merged: dict[str, Any] = {
        "openapi": "3.0.3",
        "info": main_info or {
            "title": "InvestKit API",
            "description": "InvestKit 统一 API 文档",
            "version": "1.0.0",
        },
        "paths": {},
        "components": {
            "schemas": {},
            "securitySchemes": {},
        },
        "tags": [],
    }

    existing_tags = set()

    for spec in specs:
        if not spec:
            continue

        prefix = spec.get("_prefix", "")

        if "paths" in spec:
            for path, methods in spec["paths"].items():
                new_path = f"{prefix}{path}" if prefix else path
                merged["paths"][new_path] = methods

        if "components" in spec:
            if "schemas" in spec["components"]:
                merged["components"]["schemas"].update(spec["components"]["schemas"])
            if "securitySchemes" in spec["components"]:
                merged["components"]["securitySchemes"].update(
                    spec["components"]["securitySchemes"]
                )

        if "tags" in spec:
            for tag in spec["tags"]:
                tag_name = tag.get("name")
                if tag_name and tag_name not in existing_tags:
                    existing_tags.add(tag_name)
                    merged["tags"].append(tag)

    return merged


async def fetch_openapi_spec(service: APIService) -> Optional[dict]:
    """
    获取服务的 OpenAPI 规范

    Args:
        service: API 服务定义

    Returns:
        OpenAPI 规范字典
    """
    try:
        import httpx

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{service.url}{service.openapi_url}")
            response.raise_for_status()
            spec = response.json()
            spec["_prefix"] = service.prefix
            spec["_service"] = service.name
            return spec
    except Exception as e:
        print(f"Failed to fetch OpenAPI spec from {service.name}: {e}")
        return None


def load_openapi_spec_from_file(file_path: str) -> Optional[dict]:
    """
    从文件加载 OpenAPI 规范

    Args:
        file_path: 文件路径

    Returns:
        OpenAPI 规范字典
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return None

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load OpenAPI spec from {file_path}: {e}")
        return None


async def aggregate_openapi_docs(
    services: Optional[List[APIService]] = None,
    main_info: Optional[dict] = None,
) -> dict:
    """
    聚合所有服务的 OpenAPI 文档

    Args:
        services: 服务列表 (默认使用 INVESTKIT_SERVICES)
        main_info: 主信息

    Returns:
        聚合后的 OpenAPI 规范
    """
    services = services or INVESTKIT_SERVICES
    specs = []

    for service in services:
        if service.enabled:
            spec = await fetch_openapi_spec(service)
            if spec:
                specs.append(spec)

    return merge_openapi_specs(specs, main_info)


def aggregate_from_files(
    spec_files: List[tuple],
    main_info: Optional[dict] = None,
) -> dict:
    """
    从文件聚合 OpenAPI 文档

    Args:
        spec_files: [(文件路径, 路径前缀), ...]
        main_info: 主信息

    Returns:
        聚合后的 OpenAPI 规范
    """
    specs = []

    for file_path, prefix in spec_files:
        spec = load_openapi_spec_from_file(file_path)
        if spec:
            spec["_prefix"] = prefix
            specs.append(spec)

    return merge_openapi_specs(specs, main_info)
