import pandas as pd
import pytest

from src.data.validate import assert_valid, check_index


def make(freq="1h", n=48):
    idx = pd.date_range("2024-01-01", periods=n, freq=freq, tz="UTC")
    return pd.DataFrame({"price_usd_mwh": 30.0}, index=idx)


def test_clean_frame_passes():
    assert_valid(make(), price_col="price_usd_mwh")


def test_duplicates_and_gaps_detected():
    df = make()
    bad = pd.concat([df.iloc[:10], df.iloc[11:], df.iloc[[5]]]).sort_index()
    problems = check_index(bad)
    assert any("duplicate" in p for p in problems)
    assert any("missing" in p for p in problems)


def test_non_utc_index_rejected():
    df = make()
    df.index = df.index.tz_convert("America/Chicago")
    with pytest.raises(ValueError):
        assert_valid(df)
