"""Shared time helpers so everyone handles UTC / DST / hour-ending the same way.

ERCOT labels hourly intervals by their END ("hour ending 1" = 00:00-01:00 local).
Convention here: convert to the interval START in UTC and store as `timestamp_utc`.
"""
import pandas as pd

from src.config import CAISO_TZ, ERCOT_TZ


def hour_ending_to_naive_end(dates, hour_ending) -> pd.Series:
    """Naive local interval-END timestamp from a date and hour-ending 1..24.

    HE24 becomes 00:00 of the next day, which is correct for an interval end.
    """
    dates = pd.to_datetime(pd.Series(dates)).dt.normalize()
    he = pd.Series(hour_ending).astype(int)
    return dates + pd.to_timedelta(he, unit="h")


def localize_to_utc(naive_ts, tz: str = ERCOT_TZ, ambiguous="infer") -> pd.DatetimeIndex:
    """Localize naive local timestamps and convert to UTC.

    `ambiguous="infer"` works when the repeated fall-back hour appears in order.
    If a source provides a DST flag, pass a boolean array instead (True = DST).
    Nonexistent spring-forward times are shifted forward.
    """
    idx = pd.DatetimeIndex(naive_ts)
    return idx.tz_localize(tz, ambiguous=ambiguous, nonexistent="shift_forward").tz_convert("UTC")


def interval_end_to_start_utc(naive_end, tz: str = ERCOT_TZ, interval="1h", ambiguous="infer") -> pd.DatetimeIndex:
    """Naive local interval-end -> UTC interval-start (subtract AFTER converting to UTC, so DST-safe)."""
    return localize_to_utc(naive_end, tz=tz, ambiguous=ambiguous) - pd.Timedelta(interval)


def ercot_hour_ending_to_utc_start(dates, hour_ending, ambiguous="infer") -> pd.DatetimeIndex:
    return interval_end_to_start_utc(hour_ending_to_naive_end(dates, hour_ending), tz=ERCOT_TZ, ambiguous=ambiguous)


def caiso_naive_start_to_utc(naive_start, ambiguous="infer") -> pd.DatetimeIndex:
    """CAISO timestamps are Pacific; if a source gives interval START, just localize."""
    return localize_to_utc(naive_start, tz=CAISO_TZ, ambiguous=ambiguous)


def to_local_central(utc_index) -> pd.DatetimeIndex:
    return pd.DatetimeIndex(utc_index).tz_convert(ERCOT_TZ)
