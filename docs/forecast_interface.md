# Forecast file format (Forecasting → Optimization)

Parquet, one file per model: `data/processed/forecasts/<model_name>.parquet`

| Column | Description |
|---|---|
| timestamp_utc | interval start being forecast |
| hub | settlement point |
| forecast_usd_mwh | point forecast |
| q10, q50, q90 | optional quantiles |
| model | model name |
| issued_at_utc | when the forecast would have been made |
