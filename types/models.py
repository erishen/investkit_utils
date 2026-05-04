"""数据类定义"""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, Literal, List

from investkit_utils.types.enums import (
    SignalType,
    OrderType,
    OrderStatus,
    Market,
)


@dataclass
class StockInfo:
    """股票信息"""
    code: str
    name: str
    market: Market
    industry: Optional[str] = None
    sector: Optional[str] = None
    list_date: Optional[date] = None
    total_shares: Optional[float] = None
    float_shares: Optional[float] = None

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "name": self.name,
            "market": self.market.value,
            "industry": self.industry,
            "sector": self.sector,
            "list_date": self.list_date.isoformat() if self.list_date else None,
            "total_shares": self.total_shares,
            "float_shares": self.float_shares,
        }


@dataclass
class Price:
    """价格数据"""
    open: float
    high: float
    low: float
    close: float
    volume: float
    amount: Optional[float] = None
    timestamp: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume,
            "amount": self.amount,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }


@dataclass
class TradeSignal:
    """交易信号"""
    symbol: str
    signal_type: SignalType
    price: Optional[float] = None
    quantity: Optional[float] = None
    confidence: Optional[float] = None
    reason: Optional[str] = None
    indicators: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "symbol": self.symbol,
            "signal_type": self.signal_type.value,
            "price": self.price,
            "quantity": self.quantity,
            "confidence": self.confidence,
            "reason": self.reason,
            "indicators": self.indicators,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class Position:
    """持仓信息"""
    symbol: str
    quantity: float
    cost_price: float
    current_price: Optional[float] = None
    market_value: Optional[float] = None
    profit_loss: Optional[float] = None
    profit_loss_pct: Optional[float] = None

    def __post_init__(self):
        if self.current_price is not None:
            self.market_value = self.quantity * self.current_price
            self.profit_loss = (self.current_price - self.cost_price) * self.quantity
            if self.cost_price > 0:
                self.profit_loss_pct = (self.current_price - self.cost_price) / self.cost_price * 100

    def to_dict(self) -> dict:
        return {
            "symbol": self.symbol,
            "quantity": self.quantity,
            "cost_price": self.cost_price,
            "current_price": self.current_price,
            "market_value": self.market_value,
            "profit_loss": self.profit_loss,
            "profit_loss_pct": self.profit_loss_pct,
        }


@dataclass
class Portfolio:
    """投资组合"""
    name: str
    positions: List[Position] = field(default_factory=list)
    cash: float = 0.0
    total_value: Optional[float] = None
    total_cost: Optional[float] = None
    total_profit_loss: Optional[float] = None
    total_profit_loss_pct: Optional[float] = None

    def calculate_totals(self) -> None:
        """计算组合总计"""
        self.total_cost = sum(p.quantity * p.cost_price for p in self.positions)
        position_value = sum(p.market_value or 0 for p in self.positions)
        self.total_value = position_value + self.cash

        if self.total_cost and self.total_cost > 0:
            self.total_profit_loss = self.total_value - self.total_cost
            self.total_profit_loss_pct = (self.total_value - self.total_cost) / self.total_cost * 100

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "positions": [p.to_dict() for p in self.positions],
            "cash": self.cash,
            "total_value": self.total_value,
            "total_cost": self.total_cost,
            "total_profit_loss": self.total_profit_loss,
            "total_profit_loss_pct": self.total_profit_loss_pct,
        }


@dataclass
class Order:
    """订单"""
    symbol: str
    side: Literal["BUY", "SELL"]
    order_type: OrderType
    quantity: float
    price: Optional[float] = None
    status: OrderStatus = OrderStatus.PENDING
    order_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    filled_at: Optional[datetime] = None
    filled_price: Optional[float] = None
    filled_quantity: Optional[float] = None

    def to_dict(self) -> dict:
        return {
            "symbol": self.symbol,
            "side": self.side,
            "order_type": self.order_type.value,
            "quantity": self.quantity,
            "price": self.price,
            "status": self.status.value,
            "order_id": self.order_id,
            "created_at": self.created_at.isoformat(),
            "filled_at": self.filled_at.isoformat() if self.filled_at else None,
            "filled_price": self.filled_price,
            "filled_quantity": self.filled_quantity,
        }


@dataclass
class RiskMetrics:
    """风险指标"""
    symbol: Optional[str] = None
    var_95: Optional[float] = None
    var_99: Optional[float] = None
    max_drawdown: Optional[float] = None
    sharpe_ratio: Optional[float] = None
    sortino_ratio: Optional[float] = None
    volatility: Optional[float] = None
    beta: Optional[float] = None
    alpha: Optional[float] = None

    def to_dict(self) -> dict:
        return {
            "symbol": self.symbol,
            "var_95": self.var_95,
            "var_99": self.var_99,
            "max_drawdown": self.max_drawdown,
            "sharpe_ratio": self.sharpe_ratio,
            "sortino_ratio": self.sortino_ratio,
            "volatility": self.volatility,
            "beta": self.beta,
            "alpha": self.alpha,
        }


@dataclass
class MLPrediction:
    """ML 预测结果"""
    symbol: str
    prediction: float
    confidence: float
    model_name: str
    features_used: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "symbol": self.symbol,
            "prediction": self.prediction,
            "confidence": self.confidence,
            "model_name": self.model_name,
            "features_used": self.features_used,
            "timestamp": self.timestamp.isoformat(),
        }
