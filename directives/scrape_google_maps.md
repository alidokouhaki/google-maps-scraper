# Google Maps Scraper Directive

**Goal:** Scrape business listings from Google Maps based on "City" and "Field of Activity".

**Input:**
- City (شهر)
- Business Category / Field of Activity (حوزه فعالیت)

**Tool to Run:**
`execution/scrape_google_maps.py`

**Usage:**
```bash
python execution/scrape_google_maps.py --city "Isfahan" --category "شرکت حسابداری"
```

**Data Extraction Fields:**
- Business Name
- Rating
- Total Reviews Count
- Category / Business Type
- Address / Location Details
- Phone Number
- Website URL
- Open Status

**Output:**
- The script automatically navigates through results and scrapes all listings.
- Data is saved into `.tmp/output_directory_data.xlsx`.
- Script pauses for human-in-the-loop review before continuing.

**Notes for Error Handling / Self-Annealing:**
- Google Maps DOM is obfuscated and frequently changes.
- If elements are not found, check if class names like `F7nice` (Rating) or `DkEaL` (Category) have changed, or rely on `data-item-id`.
- For anti-bot, headless is set to `False` by default to mimic real browser visually, but can be switched to `True`.
