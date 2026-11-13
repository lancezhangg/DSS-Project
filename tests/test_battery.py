import numpy as np

from src.optimization.battery import optimize_battery, realized_revenue


def two_price_day():
    p = np.full(24, 30.0)
    p[0:6] = 10.0
    p[16:20] = 100.0
    return p


def test_flat_prices_earn_nothing():
    d = optimize_battery(np.full(24, 50.0))
    assert abs(realized_revenue(np.full(24, 50.0), d)) < 1e-4


def test_profits_from_spread_and_respects_limits():
    p = two_price_day()
    d = optimize_battery(p, power_mw=100, energy_mwh=200, rte=0.85, max_cycles_per_day=1.0)
    assert realized_revenue(p, d) > 0
    assert d.discharge_mw.max() <= 100 + 1e-6
    assert d.soc_mwh.min() >= -1e-6 and d.soc_mwh.max() <= 200 + 1e-6
    assert d.discharge_mw.sum() <= 200 + 1e-6          # <= 1 cycle/day
    assert d.soc_mwh[-1] >= d.soc_mwh[0] - 1e-6        # ends at least as full


def test_forecast_error_cannot_beat_perfect_foresight():
    actual = two_price_day()
    wrong = actual[::-1].copy()
    rev_pf = realized_revenue(actual, optimize_battery(actual))
    rev_fc = realized_revenue(actual, optimize_battery(wrong))
    assert rev_fc <= rev_pf + 1e-6
