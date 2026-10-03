# Real world data

Kommineni Group is simulated, but the world it lives in is real. Free public data feeds the source systems, so the business reacts to what actually happens in the economy, the weather and the calendar.

The rule: the outside data is real, the business reaction is simulated.

## Feeds

| Feed | Source (free) | What it changes |
|---|---|---|
| Interest rates | FRED (Federal Reserve Bank of St. Louis), free API key | Meel Pay loan approvals and rates, Meel Motors sales |
| Consumer credit, unemployment, inflation | FRED, BLS | How much people spend across every division |
| Gas prices | US Energy Information Administration (EIA), free API key | Mix of hybrids vs trucks sold, Meel Move fuel costs |
| Weather | Open-Meteo, no key for non-commercial use | Showroom traffic, service jobs (dead batteries, flat tires), delivery delays |
| Severe storms | NOAA | Branch closures, late shipments |
| Vehicle recalls | NHTSA recalls API | Waves of recall service jobs for affected models |
| Exchange rates | European Central Bank daily reference rates | Meel Cart worldwide prices and refunds |
| Holidays | `holidays` Python package | Closed days, Black Friday, holiday rush, country-specific holidays |
| Population and income by area | US Census Bureau API | How big and busy each branch and clinic is |
| Drug recalls, adverse events | openFDA | Meel Care prescriptions and pharmacy stock |
| Hospital and Medicare data | CMS public data | Realistic Meel Care visit types, costs and claim amounts |

## How it works

1. A daily job pulls each feed into `shared/world/` as its own bronze table.
2. The source systems read those tables when they simulate the day.
3. The pipeline keeps the world data too, so dashboards can explain why numbers moved.

Pulling these feeds is a set of problems by itself: API keys kept secret, rate limits, feeds that publish late, values revised after release (FRED does this), and holidays when a feed doesn't update.

## Worldwide orders (Meel Cart)

Meel Cart sells in the US, Canada, the UK, Europe and India. That brings:

- Many currencies, converted with the daily rate of the order date
- Time zones. An order at 11 pm in Chicago is already the next day in London. Finance reports in US Central time.
- US sales tax, UK and EU VAT, India GST
- Local address, phone and name formats, plus names in non-Latin scripts
- Privacy rules by region, such as GDPR deletion requests
