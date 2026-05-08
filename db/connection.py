import sqlite3
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

from .paths import get_asset_lens_db_path


@contextmanager
def db_connection(db_path: Path | None = None) -> Generator[sqlite3.Connection, None, None]:
    if db_path is None:
        db_path = get_asset_lens_db_path()
    conn = sqlite3.connect(str(db_path))
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


@contextmanager
def db_transaction(db_path: Path | None = None) -> Generator[sqlite3.Connection, None, None]:
    if db_path is None:
        db_path = get_asset_lens_db_path()
    conn = sqlite3.connect(str(db_path))
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
