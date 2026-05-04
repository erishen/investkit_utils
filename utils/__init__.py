"""
InvestKit 共享工具函数

提供各项目通用的工具函数。

模块:
- datetime_utils: 日期时间工具
- retry: 重试装饰器
- validators: 数据验证器
- numeric: 数值计算工具
- string_utils: 字符串工具
- financial: 金融计算工具
- data_utils: 数据处理工具
- file_utils: 文件工具
"""

from investkit_utils.utils.datetime_utils import (
    parse_date,
    format_date,
    get_trading_days,
    is_trading_day,
)

from investkit_utils.utils.retry import (
    retry,
    retry_async,
)

from investkit_utils.utils.validators import (
    validate_stock_code,
    validate_amount,
    validate_percentage,
)

from investkit_utils.utils.numeric import (
    safe_divide,
    round_to,
    percentage_change,
)

from investkit_utils.utils.string_utils import (
    truncate_string,
    mask_sensitive,
)

from investkit_utils.utils.financial import (
    calculate_irr,
    calculate_cagr,
    calculate_sharpe_ratio,
    calculate_max_drawdown,
    calculate_win_rate,
    calculate_profit_factor,
    calculate_position_size,
    calculate_compound_interest,
)

from investkit_utils.utils.data_utils import (
    deep_merge,
    flatten_dict,
    unflatten_dict,
    chunk_list,
    unique_list,
    group_by,
    safe_get,
    to_json_serializable,
    to_decimal,
    batch_process,
)

from investkit_utils.utils.file_utils import (
    ensure_dir,
    read_json,
    write_json,
    read_text,
    write_text,
    read_lines,
    get_file_info,
    format_file_size,
    clean_dir,
    copy_file,
    move_file,
    find_files,
    get_latest_file,
)


__all__ = [
    "parse_date",
    "format_date",
    "get_trading_days",
    "is_trading_day",
    "retry",
    "retry_async",
    "validate_stock_code",
    "validate_amount",
    "validate_percentage",
    "safe_divide",
    "round_to",
    "percentage_change",
    "truncate_string",
    "mask_sensitive",
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
    "unflatten_dict",
    "chunk_list",
    "unique_list",
    "group_by",
    "safe_get",
    "to_json_serializable",
    "to_decimal",
    "batch_process",
    "ensure_dir",
    "read_json",
    "write_json",
    "read_text",
    "write_text",
    "read_lines",
    "get_file_info",
    "format_file_size",
    "clean_dir",
    "copy_file",
    "move_file",
    "find_files",
    "get_latest_file",
]
