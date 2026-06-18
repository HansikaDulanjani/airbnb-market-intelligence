# Business Domain Context - Bangkok Airbnb Market Intelligence

## 1. What is Inside Airbnb?
Inside Airbnb is an independent, non-commercial project that collects 
and publishes publicly available Airbnb listing data. The data is 
scraped periodically and made available for public analysis.

## 2. Core Entities

### Listing
A listing represents a property advertised on Airbnb by a host.
Each listing has a unique ID, location, room type, pricing, 
availability, and review scores. A listing is the central entity 
connecting all other datasets.

### Host
A host is an individual or organization that owns and manages 
one or more listings. Hosts can be casual individuals renting 
out a spare room or professional operators managing dozens of 
properties.

### Review
A review is written by a guest after completing a stay. Reviews 
contain a date, reviewer identity, and written comments. They 
reflect guest satisfaction and are a proxy for actual bookings.

### Calendar
The calendar represents daily availability and pricing for each 
listing over a future 12-month period. It shows whether a listing 
is available or blocked on any given date.

## 3. Business Questions This Dataset Can Answer
- Which neighbourhoods have the highest average listing prices?
- What room types are most common in Bangkok?
- How does pricing vary across seasons?
- Which hosts dominate the market (multi-listing operators)?
- What factors influence review scores?
- How far in advance do hosts block their calendars?

## 4. Dataset Scope
- City: Bangkok, Thailand
- Source: Inside Airbnb (insideairbnb.com)
- Scrape Date: September 2025
- Total Listings: 28,806
- Total Calendar Records: 10,514,202
- Total Reviews: 583,333