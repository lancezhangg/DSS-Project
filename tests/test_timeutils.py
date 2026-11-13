import pandas as pd

from src.data.timeutils import ercot_hour_ending_to_utc_start, localize_to_utc


def test_summer_hour_ending_1():
    # HE1 on 2024-07-01 = 00:00-01:00 CDT (UTC-5) -> start 05:00 UTC
    out = ercot_hour_ending_to_utc_start(["2024-07-01"], [1])
    assert out[0] == pd.Timestamp("2024-07-01 05:00", tz="UTC")


def test_winter_hour_ending_24_rolls_to_next_day_end():
    # HE24 on 2024-01-15 = 23:00-24:00 CST (UTC-6) -> start 05:00 UTC on Jan 16
    out = ercot_hour_ending_to_utc_start(["2024-01-15"], [24])
    assert out[0] == pd.Timestamp("2024-01-16 05:00", tz="UTC")


def test_fall_back_roundtrip_has_no_duplicates():
    utc = pd.date_range("2024-11-03 04:00", periods=8, freq="h", tz="UTC")
    local_naive = utc.tz_convert("America/Chicago").tz_localize(None)
    back = localize_to_utc(local_naive)
    assert back.equals(utc)
    assert not back.duplicated().any()
