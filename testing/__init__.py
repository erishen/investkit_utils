"""
InvestKit 测试工具函数

提供各项目共享的测试工具和 fixtures。

使用示例:
    from investkit_utils.testing import mock_response, assert_dict_equal, temp_directory
"""

from investkit_utils.testing.assertions import (
    assert_almost_equal,
    assert_dict_equal,
    assert_list_contains,
    assert_raises,
)
from investkit_utils.testing.data_generators import (
    generate_test_portfolio,
    generate_test_stock_data,
)
from investkit_utils.testing.fixtures import (
    temp_directory,
    temp_file,
)
from investkit_utils.testing.mocks import (
    create_mock_cache,
    create_mock_db_session,
    mock_response,
)

__all__ = [
    "mock_response",
    "create_mock_db_session",
    "create_mock_cache",
    "assert_dict_equal",
    "assert_almost_equal",
    "assert_list_contains",
    "assert_raises",
    "temp_directory",
    "temp_file",
    "generate_test_stock_data",
    "generate_test_portfolio",
]
