# Project Plan

## Research questions
1. How much revenue does a battery lose because it cannot see prices ahead of time, and which forecasting improvements recover the most?
2. How fast do price spreads shrink as storage grows, and what does that mean for the next project?

## Schedule
| Week | Focus | Milestone (written, due at end of week) |
|---|---|---|
| 4 | Context, plan | Plan, conventions, inventory |
| 5 | Source + start cleaning | Raw data, cleaned per-source files, draft merged tables |
| 6 | Finish cleaning, start analyses | Final tables; baseline forecasts; full backtest |
| 7 | Analyses + visualizations | Results tables and figures |
| 8 | Deliverables | Dashboard + paper draft |
| 9 | Finish + symposium | Final repo, paper, presentation |

## Owners and tasks
See README team table and GitHub Issues.

## Risks and fallbacks
- ERCOT API credential delays → bulk downloads from the ERCOT portal.
- Timestamp errors → shared `timeutils.py` + validation tests + spot-checks against raw files.
- Scope creep → forecasting does not start until hub price table passes validation.
