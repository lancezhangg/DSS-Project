# Data Dictionary

| Column | Description | Unit | Source | Timestamp convention | Known at decision time? (vs day-ahead) |
|---|---|---|---|---|---|
| timestamp_utc | Interval start | UTC | all | interval start | n/a |
| dam_price_usd_mwh | Day-ahead hub SPP | $/MWh | ERCOT | start | Known after DAM clears (not an input to the DAM decision) |
| rtm_price_usd_mwh | Real-time hub SPP (hourly mean) | $/MWh | ERCOT | start | No (realized later) |
