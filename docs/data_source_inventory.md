# Data Source Inventory

| Source | Owner | Access method | Variables | URL | Known issues |
|---|---|---|---|---|---|
| ERCOT DAM/RTM SPP (hubs) | Rhianna | gridstatus / ERCOT API | hourly DAM, 15-min RTM prices | https://data.ercot.com/ , https://apiexplorer.ercot.com/ | credentials; format changes across years |
| ERCOT load + forecasts | Liam | ERCOT API / gridstatus | load actual, load forecast | https://data.ercot.com/ | label forecast vs actual |
| ERCOT wind/solar + forecasts | Liam | ERCOT API / gridstatus | generation actual, forecast | https://data.ercot.com/ | |
| ERCOT ancillary prices | Liam | ERCOT API | price by product | https://data.ercot.com/ | products change by year (ECRS added 2023) |
| Weather | Tommy | Open-Meteo | temp, wind, irradiance | https://open-meteo.com/en/docs | observed vs historical forecast |
| Henry Hub gas | Tommy | EIA API | daily spot | https://www.eia.gov/opendata/ | non-trading days; Texas hubs may differ |
| Storage capacity (ERCOT) | Tommy | ERCOT reports + EIA-860M | operating vs planned MW | https://www.ercot.com/gridinfo/resource , https://www.eia.gov/electricity/data/eia860m/ | planned ≠ built |
| CAISO prices + storage | Tommy | OASIS / gridstatus | DAM/RT prices, battery MW | http://oasis.caiso.com/ | Pacific time; rate limits |
