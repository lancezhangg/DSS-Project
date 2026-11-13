"""Battery dispatch via cvxpy. The optimizer SEES `prices`; revenue is SETTLED at actual prices."""
from dataclasses import dataclass

import cvxpy as cp
import numpy as np


@dataclass
class Dispatch:
    charge_mw: np.ndarray
    discharge_mw: np.ndarray
    soc_mwh: np.ndarray
    objective: float


def optimize_battery(
    prices,
    power_mw: float = 100.0,
    energy_mwh: float = 200.0,
    rte: float = 0.85,
    soc0_frac: float = 0.5,
    max_cycles_per_day: float = 1.0,
    dt_hours: float = 1.0,
    wear_cost_per_mwh: float = 0.0,
) -> Dispatch:
    """Maximize price-weighted net discharge subject to power, energy, efficiency, and cycle limits.

    Notes / simplifications: losses split evenly between charge and discharge; degradation is a
    cycle cap plus optional wear cost; the LP may charge and discharge in the same interval when
    prices are negative (harmless for revenue but unphysical); price-taker assumption.
    """
    prices = np.asarray(prices, dtype=float)
    T = len(prices)
    eta = np.sqrt(rte)
    days = T * dt_hours / 24.0

    charge = cp.Variable(T, nonneg=True)
    discharge = cp.Variable(T, nonneg=True)
    soc = cp.Variable(T + 1)

    constraints = [
        soc[0] == soc0_frac * energy_mwh,
        soc >= 0,
        soc <= energy_mwh,
        charge <= power_mw,
        discharge <= power_mw,
        soc[1:] == soc[:-1] + eta * charge * dt_hours - discharge * dt_hours / eta,
        cp.sum(discharge) * dt_hours <= max_cycles_per_day * energy_mwh * days,
        soc[T] >= soc[0],  # don't "sell the tank" at the end of the horizon
    ]
    revenue = cp.sum(cp.multiply(prices, discharge - charge)) * dt_hours
    wear = wear_cost_per_mwh * cp.sum(discharge) * dt_hours
    problem = cp.Problem(cp.Maximize(revenue - wear), constraints)
    problem.solve()
    if problem.status not in ("optimal", "optimal_inaccurate"):
        raise RuntimeError(f"Optimization failed: {problem.status}")

    return Dispatch(charge.value, discharge.value, soc.value, float(problem.value))


def realized_revenue(actual_prices, dispatch: Dispatch, dt_hours: float = 1.0, wear_cost_per_mwh: float = 0.0) -> float:
    """Revenue of a chosen schedule settled at ACTUAL prices."""
    actual = np.asarray(actual_prices, dtype=float)
    net = dispatch.discharge_mw - dispatch.charge_mw
    return float(np.sum(actual * net) * dt_hours - wear_cost_per_mwh * np.sum(dispatch.discharge_mw) * dt_hours)
