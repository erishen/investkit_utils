"""
InvestKit 共享模块

提供各项目共享的配置、日志、缓存、工具、异常、类型定义和测试工具。

模块:
- config: 配置管理
- cache: 缓存抽象层
- logging: 统一日志
- api_docs: API 文档聚合
- utils: 通用工具函数
- exceptions: 统一异常处理
- types: 共享类型定义
- testing: 测试工具函数
- db: 数据库模型、连接管理、路径配置
"""

from investkit_utils.api_docs import (
    INVESTKIT_SERVICES,
    APIService,
    ServiceInfo,
    ServiceRegistry,
    aggregate_openapi_docs,
    get_service_registry,
    serve_aggregated_docs,
)
from investkit_utils.cache import (
    CacheBackend,
    MemoryCache,
    cached,
    cached_async,
    get_cache,
)
from investkit_utils.config import (
    Config,
    get_config,
    reload_config,
    set_config_path,
)
from investkit_utils.exceptions import (
    InvestKitError,
    NotFoundError,
    ValidationError,
    handle_exception,
)
from investkit_utils.log_utils import get_logger, setup_logging
from investkit_utils.types import (
    OrderType,
    Portfolio,
    Position,
    SignalType,
    StockInfo,
    TradeSignal,
)
from investkit_utils.utils import (
    calculate_cagr,
    calculate_compound_interest,
    calculate_irr,
    calculate_max_drawdown,
    calculate_position_size,
    calculate_profit_factor,
    calculate_sharpe_ratio,
    calculate_win_rate,
    chunk_list,
    deep_merge,
    ensure_dir,
    find_files,
    flatten_dict,
    format_date,
    format_file_size,
    group_by,
    parse_date,
    percentage_change,
    read_json,
    read_text,
    retry,
    round_to,
    safe_divide,
    safe_get,
    to_json_serializable,
    unique_list,
    validate_stock_code,
    write_json,
    write_text,
)

try:
    from investkit_utils.db import (
        DATA_DIR,
        EXCLUDED_KEYWORDS,
        Base,
        DataSyncLog,
        MLModel,
        PredictionRecord,
        StockKline,
        db_connection,
        db_transaction,
        ensure_data_dir,
        get_asset_lens_db_path,
        get_db_path,
        get_stock_analysis_db_path,
        get_stock_klines_db_path,
        init_database,
        is_excluded_stock,
    )
    from investkit_utils.db import (
        StockInfo as DBStockInfo,
    )
except ImportError:
    pass
__version__ = "1.0.0"
__all__ = [
    "Config",
    "get_config",
    "reload_config",
    "set_config_path",
    "CacheBackend",
    "MemoryCache",
    "get_cache",
    "cached",
    "cached_async",
    "get_logger",
    "setup_logging",
    "APIService",
    "INVESTKIT_SERVICES",
    "aggregate_openapi_docs",
    "serve_aggregated_docs",
    "ServiceRegistry",
    "ServiceInfo",
    "get_service_registry",
    "parse_date",
    "format_date",
    "retry",
    "validate_stock_code",
    "safe_divide",
    "round_to",
    "percentage_change",
    "calculate_irr",
    "calculate_cagr",
    "calculate_sharpe_ratio",
    "calculate_max_drawdown",
    "calculate_win_rate",
    "calculate_profit_factor",
    "calculate_position_size",
    "calculate_compound_interest",
    "deep_merge",
    "flatten_dict",
    "chunk_list",
    "unique_list",
    "group_by",
    "safe_get",
    "to_json_serializable",
    "ensure_dir",
    "read_json",
    "write_json",
    "read_text",
    "write_text",
    "format_file_size",
    "find_files",
    "InvestKitError",
    "ValidationError",
    "NotFoundError",
    "handle_exception",
    "SignalType",
    "OrderType",
    "StockInfo",
    "TradeSignal",
    "Position",
    "Portfolio",
    "Base",
    "DATA_DIR",
    "DataSyncLog",
    "EXCLUDED_KEYWORDS",
    "MLModel",
    "PredictionRecord",
    "DBStockInfo",
    "StockKline",
    "db_connection",
    "db_transaction",
    "ensure_data_dir",
    "get_asset_lens_db_path",
    "get_db_path",
    "get_stock_analysis_db_path",
    "get_stock_klines_db_path",
    "init_database",
    "is_excluded_stock",
]
