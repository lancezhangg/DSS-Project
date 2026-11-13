# What Is a Grid Battery Worth in ERCOT?

How much revenue does a battery lose because it can't see future prices, and how fast do its earning opportunities shrink as more storage is built? We pull ERCOT, weather, gas, and CAISO data, build forecasts from simple baselines to gradient-boosted trees and quantile regression, and run each through a cvxpy battery simulation against a perfect-foresight benchmark. Forecasts are scored by the **revenue a battery earns when it follows them**, not just by error metrics. A regression of price spreads on installed storage, compared with California, shows how quickly spreads erode.

**Deliverables:** this reproducible repo, a Streamlit dashboard for backtesting battery strategies, and a short paper for developers and lenders.

## Team

| Member | Role | GitHub | Owns |
|---|---|---|---|
| Lance Zhang | Project Leader | TODO | Plan, conventions, config, repo, merge review |
| Rhianna Amador | ERCOT prices | TODO | DAM/RTM hub prices, hourly/daily tables |
| Liam Horton | ERCOT fundamentals | TODO | Load, wind, solar (+forecasts), ancillary prices, information timeline |
| Tommy Kann | Gas, storage, CAISO, weather | t-kann | Henry Hub, weather, storage capacity, CAISO, calendar features |
| Juliette Goldstein | TBD | TODO | TBD |
| Lara Lel | TBD | TODO | TBD (optimization owner: toy battery model, tests, exploratory charts) |

## Timeline

| Week | Focus |
|---|---|
| 4 | Context/background, make a plan |
| 5 | Source data, start cleaning and manipulating |
| 6 | Finish cleaning, start analyses |
| 7 | Continue analyses and visualizations |
| 8 | Work on deliverables, put everything together |
| 9 | Finish deliverable, present at symposium |

## Quickstart

```bash
git clone <repo-url> && cd ercot-battery-value
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # then fill in YOUR credentials; never commit .env
pytest -q
```

## Folder guide

- `data/`: raw → interim → processed. **Not committed** (see rules below); `sample/` holds tiny committed slices for tests.
- `src/config.py`: study window, hubs, locations, battery defaults. Change settings here, not in scripts.
- `src/data/`: fetch and clean scripts (one per source), `timeutils.py` (shared UTC/DST/hour-ending helpers), `validate.py`, `features.py`, `build_tables.py`.
- `src/forecasting/`, `src/optimization/`, `src/analysis/`: modeling, battery simulation, regression.
- `tests/`, `notebooks/`, `reports/`, `app/` (dashboard), `paper/`, `docs/`.

## Working rules

- **Branches:** `feature/<name>-<task>`. Never commit to `main`; open a PR and get one review.
- **Data:** don't commit raw/processed data. Commit fetch scripts so anyone can regenerate. Share large files via the team drive (link: TODO).
- **Time:** store everything in UTC as `timestamp_utc`. Always use `src/data/timeutils.py`.
- **Files:** parquet, named `source_dataset_stage.parquet`. Columns in snake_case with units (`price_usd_mwh`, `load_mw`).
- **Never** clip or drop negative prices/spikes, and never fill price gaps silently.
- **Notebooks:** `NN_initials_topic.ipynb`; clear outputs before committing (`nbstripout --install`). Reusable code goes in `src/`.
- Log every judgment call in `docs/assumptions_log.md` in the same PR. Run `pytest` before pushing.
- **Secrets:** credentials live only in `.env`. If one is committed by accident, rotate it immediately.
