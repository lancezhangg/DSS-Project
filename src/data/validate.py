"""Reusable validation checks. Call on every cleaned dataset; raise on failure."""
import pandas as pd

from src.config import PRICE_LOWER_BOUND_USD_MWH, PRICE_UPPER_BOUND_USD_MWH


def check_index(df: pd.DataFrame, freq: str = "1h") -> list[str]:
    """Return a list of problems with a UTC DatetimeIndex (empty list = OK)."""
    problems = []
    idx = df.index
    if not isinstance(idx, pd.DatetimeIndex) or idx.tz is None or str(idx.tz) != "UTC":
        problems.append("index is not a UTC DatetimeIndex")
        return problems
    if idx.duplicated().any():
        problems.append(f"{int(idx.duplicated().sum())} duplicate timestamps")
    if not idx.is_monotonic_increasing:
        problems.append("index is not sorted")
    expected = pd.date_range(idx.min(), idx.max(), freq=freq, tz="UTC")
    missing = expected.difference(idx)
    if len(missing):
        problems.append(f"{len(missing)} missing timestamps (first: {missing[0]})")
    return problems


def check_price_range(series: pd.Series) -> list[str]:
    """Flags values outside plausibility bounds. Does NOT modify data; spikes are signal."""
    problems = []
    n_high = int((series > PRICE_UPPER_BOUND_USD_MWH).sum())
    n_low = int((series < PRICE_LOWER_BOUND_USD_MWH).sum())
    if n_high:
        problems.append(f"{n_high} values above {PRICE_UPPER_BOUND_USD_MWH}")
    if n_low:
        problems.append(f"{n_low} values below {PRICE_LOWER_BOUND_USD_MWH}")
    return problems


def assert_valid(df: pd.DataFrame, price_col: str | None = None, freq: str = "1h") -> None:
    problems = check_index(df, freq)
    if price_col:
        problems += check_price_range(df[price_col])
    if problems:
        raise ValueError("Validation failed: " + "; ".join(problems))
