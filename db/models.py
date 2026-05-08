import warnings
from datetime import datetime
from typing import Any

from sqlalchemy import Boolean, Column, DateTime, Float, Index, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

warnings.filterwarnings("ignore", category=DeprecationWarning, module="sqlalchemy")

Base = declarative_base()


class StockKline(Base):
    __tablename__ = "stock_klines"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(20), nullable=False)
    date = Column(String(10), nullable=False)
    open = Column(Float, default=0)
    close = Column(Float, default=0)
    high = Column(Float, default=0)
    low = Column(Float, default=0)
    volume = Column(Float, default=0)
    amount = Column(Float, default=0)
    amplitude = Column(Float, default=0)
    change_percent = Column(Float, default=0)
    change_amount = Column(Float, default=0)
    turnover_rate = Column(Float, default=0)
    data_source = Column(String(50), default="")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (
        Index("idx_kline_code_date", "code", "date", unique=True),
        Index("idx_kline_date", "date"),
        Index("idx_kline_code", "code"),
    )

    def to_dict(self) -> dict:
        return {
            "date": self.date, "open": self.open, "close": self.close,
            "high": self.high, "low": self.low, "volume": self.volume,
            "amount": self.amount, "amplitude": self.amplitude,
            "change_percent": self.change_percent, "change_amount": self.change_amount,
            "turnover_rate": self.turnover_rate,
        }


class StockInfo(Base):
    __tablename__ = "stock_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(50), default="")
    industry = Column(String(50), default="")
    sector = Column(String(50), default="")
    market = Column(String(20), default="")
    list_date = Column(String(10), default="")
    total_shares = Column(Float, default=0)
    float_shares = Column(Float, default=0)
    total_market_cap = Column(Float, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (Index("idx_stock_code", "code"),)


class MLModel(Base):
    __tablename__ = "ml_models"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    model_type = Column(String(50), default="lightgbm")
    version = Column(String(20), default="1.0.0")
    params = Column(Text, default="{}")
    feature_importance = Column(Text, default="{}")
    metrics = Column(Text, default="{}")
    train_samples = Column(Integer, default=0)
    train_features = Column(Integer, default=0)
    train_date_start = Column(String(10), default="")
    train_date_end = Column(String(10), default="")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    __table_args__ = (Index("idx_model_name_version", "name", "version"),)


class PredictionRecord(Base):
    __tablename__ = "prediction_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(Integer, default=0)
    code = Column(String(20), nullable=False)
    predict_date = Column(String(10), nullable=False)
    prediction = Column(Integer, default=0)
    confidence = Column(Float, default=0)
    features = Column(Text, default="{}")
    actual_result = Column(Integer, default=None)
    is_correct = Column(Boolean, default=None)
    created_at = Column(DateTime, default=datetime.now)

    __table_args__ = (
        Index("idx_pred_code_date", "code", "predict_date"),
        Index("idx_pred_model", "model_id"),
    )


class DataSyncLog(Base):
    __tablename__ = "data_sync_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data_type = Column(String(50), nullable=False)
    data_source = Column(String(50), default="")
    sync_start = Column(DateTime, nullable=False)
    sync_end = Column(DateTime, default=None)
    records_total = Column(Integer, default=0)
    records_success = Column(Integer, default=0)
    records_failed = Column(Integer, default=0)
    status = Column(String(20), default="running")
    error_message = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.now)

    __table_args__ = (Index("idx_sync_type_date", "data_type", "sync_start"),)


def init_database(db_url: str = "sqlite:///./data/asset_lens.db"):
    engine_kwargs: dict[str, Any] = {"echo": False}
    if db_url.startswith("sqlite"):
        from sqlalchemy.pool import StaticPool
        engine_kwargs["connect_args"] = {"check_same_thread": False}
        engine_kwargs["poolclass"] = StaticPool
    else:
        engine_kwargs["pool_pre_ping"] = True
        engine_kwargs["pool_size"] = 10
        engine_kwargs["max_overflow"] = 20
        engine_kwargs["pool_recycle"] = 3600
        engine_kwargs["pool_timeout"] = 30
    engine = create_engine(db_url, **engine_kwargs)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)  # noqa: N806
    return engine, Session
