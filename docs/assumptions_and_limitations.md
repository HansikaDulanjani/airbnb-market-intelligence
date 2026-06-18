# Assumptions & Limitations

## Assumptions

### Pricing
- All prices in listings.csv are in Thai Baht (THB)
- Price column contains nightly rate per listing
- Listings with null prices are excluded from price analysis

### Reviews
- Review count is used as a proxy for actual bookings
- Reviews with null comments are excluded from text analysis
- Review dates represent checkout dates approximately

### Calendar
- Calendar data represents future availability (Sep 2025 - Sep 2026)
- A listing marked "unavailable" may be booked OR blocked by host
- price and adjusted_price are null because Bangkok hosts 
  typically set prices through dynamic pricing tools not 
  reflected in scraped data

### Neighbourhoods
- neighbourhood_cleansed is used as the primary location field
- neighbourhood_group_cleansed is 100% null - Bangkok has no 
  official district groupings in Airbnb data
- host_neighbourhood is self-reported and unreliable (67% null)



## Limitations



### Data Limitations
- License column is 100% null - no regulatory data available
- calendar_updated is 100% null - scraping artifact
- No actual booking or revenue data - only estimates
- Scraped data may not reflect real-time availability

### Coverage Gaps
- ~35% of listings have no reviews (new or inactive listings)
- Host response rate missing for 5,647 hosts (19.6%)
- Historical pricing trends not available (only current snapshot)

### Scraping Artifacts
- Data represents a single point-in-time snapshot (Sep 2025)
- Prices may fluctuate significantly from scraped values
- Some listings may have been removed since scraping