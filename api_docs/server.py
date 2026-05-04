"""API 文档服务"""

from typing import Optional, List

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

from investkit_utils.api_docs.services import APIService, INVESTKIT_SERVICES
from investkit_utils.api_docs.openapi import aggregate_openapi_docs


def serve_aggregated_docs(
    services: Optional[List[APIService]] = None,
    main_info: Optional[dict] = None,
    port: int = 8080,
):
    """
    启动聚合 API 文档服务

    Args:
        services: 服务列表
        main_info: 主信息
        port: 服务端口

    Returns:
        FastAPI 应用
    """
    app = FastAPI(
        title="InvestKit API Gateway",
        description="InvestKit 统一 API 文档网关",
        docs_url=None,
        redoc_url=None,
    )

    @app.get("/", response_class=HTMLResponse)
    async def root():
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>InvestKit API Gateway</title>
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
                h1 { color: #333; }
                .service { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 8px; }
                .service h3 { margin: 0 0 10px 0; }
                .service a { color: #0066cc; text-decoration: none; }
                .service a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <h1>InvestKit API Gateway</h1>
            <p>统一 API 文档入口</p>
            <h2>可用服务</h2>
            <div class="service">
                <h3>asset-lens</h3>
                <p>个人资产操作系统 API</p>
                <a href="/docs/asset-lens">Swagger UI</a> |
                <a href="/redoc/asset-lens">ReDoc</a>
            </div>
            <div class="service">
                <h3>langchain-llm-toolkit</h3>
                <p>LLM 工具集 API</p>
                <a href="/docs/llm-toolkit">Swagger UI</a> |
                <a href="/redoc/llm-toolkit">ReDoc</a>
            </div>
            <div class="service">
                <h3>lobster</h3>
                <p>AI 助手 API</p>
                <a href="/docs/lobster">Swagger UI</a> |
                <a href="/redoc/lobster">ReDoc</a>
            </div>
            <h2>聚合文档</h2>
            <div class="service">
                <a href="/openapi.json">OpenAPI JSON</a> |
                <a href="/docs">Swagger UI (聚合)</a> |
                <a href="/redoc">ReDoc (聚合)</a>
            </div>
        </body>
        </html>
        """

    @app.get("/openapi.json")
    async def get_aggregated_openapi():
        spec = await aggregate_openapi_docs(services, main_info)
        return JSONResponse(content=spec)

    @app.get("/docs", response_class=HTMLResponse)
    async def swagger_ui():
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">
        </head>
        <body>
            <div id="swagger-ui"></div>
            <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
            <script>
                SwaggerUIBundle({
                    url: "/openapi.json",
                    dom_id: '#swagger-ui',
                    presets: [
                        SwaggerUIBundle.presets.apis,
                        SwaggerUIBundle.SwaggerUIStandalonePreset
                    ]
                })
            </script>
        </body>
        </html>
        """

    @app.get("/redoc", response_class=HTMLResponse)
    async def redoc():
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>InvestKit API Documentation</title>
            <meta charset="utf-8"/>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>body { margin: 0; padding: 0; }</style>
        </head>
        <body>
            <redoc spec-url='/openapi.json'></redoc>
            <script src="https://unpkg.com/redoc@latest/bundles/redoc.standalone.js"></script>
        </body>
        </html>
        """

    return app
