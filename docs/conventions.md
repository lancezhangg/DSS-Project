# Conventions (decide at the conventions meeting, then freeze)

| Item | Decision |
|---|---|
| Timestamp storage | UTC, column/index `timestamp_utc`; local Central column optional |
| Interval labeling | Store interval START. ERCOT "hour ending N" is converted via `timeutils.py` |
| Price unit | $/MWh |
| Price location | Hub-level to start (node-level = possible extension) |
| Study window | TODO (see `src/config.py`) |
| RT → hourly rule | TODO (e.g., simple mean of the four 15-min SPPs); keep 15-min version too |
| Spread definition | TODO (daily max−min, or perfect-foresight revenue of a reference battery) |
| Battery configs | 1/2/4-hour, 85% RTE, ≤1 cycle/day (see `src/config.py`) |
| File format / names | parquet; `source_dataset_stage.parquet` |
| Column naming | snake_case with units |
| Missing data | Never fill prices silently; document per variable |
| Extremes | Never clip/drop negative prices or spikes |
