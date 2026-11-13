"""Single source of truth for project-wide settings. Change values here, not in scripts."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
INTERIM = ROOT / "data" / "interim"
PROCESSED = ROOT / "data" / "processed"
SAMPLE = ROOT / "data" / "sample"
FIGURES = ROOT / "reports" / "figures"

# --- Study window (TODO: confirm at the conventions meeting) ---
START_DATE = "2019-01-01"
END_DATE = "2025-12-31"

# --- Time conventions ---
STORAGE_TZ = "UTC"                  # everything stored in UTC
ERCOT_TZ = "America/Chicago"        # ERCOT local (Central) time
CAISO_TZ = "America/Los_Angeles"    # CAISO local (Pacific) time
TIMESTAMP_COL = "timestamp_utc"

# --- Prices ---
# Hubs to start with (confirm exact names against the ERCOT data you pull).
ERCOT_HUBS = ["HB_NORTH", "HB_HOUSTON", "HB_SOUTH", "HB_WEST"]
# Plausibility ceiling for validation only. The cap was $9,000/MWh before Winter Storm
# Uri (Feb 2021) and later lowered; VERIFY current/historical caps before relying on this.
PRICE_UPPER_BOUND_USD_MWH = 9000.0
PRICE_LOWER_BOUND_USD_MWH = -300.0  # RT prices can go negative; verify observed minimum

# --- Weather locations (lat, lon) ---
WEATHER_LOCATIONS = {
    "houston": (29.76, -95.37),
    "dallas": (32.78, -96.80),
    "austin": (30.27, -97.74),
    "san_antonio": (29.42, -98.49),
    "west_texas": (31.99, -102.08),   # Midland area
}

# --- Battery defaults for simulation ---
BATTERY_DEFAULTS = dict(
    power_mw=100.0,
    energy_mwh=200.0,       # 2-hour battery
    rte=0.85,
    max_cycles_per_day=1.0,
    wear_cost_per_mwh=0.0,
)
BATTERY_DURATIONS_HOURS = [1, 2, 4]
