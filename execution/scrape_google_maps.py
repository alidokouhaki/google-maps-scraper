import os
import argparse
import time
import urllib.parse
from playwright.sync_api import sync_playwright
import pandas as pd

def extract_place_data(page, url):
    try:
        # ensure url has hl=en so we can parse English keywords like "Address:"
        if '?' in url:
            nav_url = url + '&hl=en'
        else:
            nav_url = url + '?hl=en'
        
        page.goto(nav_url, timeout=60000)
        page.wait_for_selector('h1', timeout=15000)
        time.sleep(2) # Let data populate
        
        name = page.locator('h1').text_content().strip()
        
        rating = ""
        reviews_count = ""
        category = ""
        address = ""
        phone = ""
        website = ""
        open_status = ""
        
        # Rating & Reviews
        f7nice = page.locator('div.F7nice')
        if f7nice.count() > 0:
            text = f7nice.first.inner_text()
            parts = text.split('\n')
            if len(parts) >= 1:
                rating = parts[0].strip()
            if len(parts) >= 2:
                reviews_count = parts[1].replace('(', '').replace(')', '').strip()
                
        # Category
        category_btn = page.locator('button.DkEaL')
        if category_btn.count() > 0:
            category = category_btn.first.inner_text().strip()
            
        # Address
        addr_btn = page.locator('button[data-item-id="address"]')
        if addr_btn.count() > 0:
            raw_address = addr_btn.first.inner_text().replace('Address:', '').strip()
            address = raw_address.split('\n')[-1].strip()

        # Phone
        phone_btn = page.locator('button[data-item-id^="phone:"]')
        if phone_btn.count() > 0:
            raw_phone = phone_btn.first.inner_text().replace('Phone:', '').strip()
            phone = raw_phone.split('\n')[-1].strip()
            
        # Website
        web_btn = page.locator('a[data-item-id="authority"]')
        if web_btn.count() > 0:
            website = web_btn.first.get_attribute('href')
            
        # Open Status
        hours_div = page.locator('div[class*="t39OBf"]')
        if hours_div.count() > 0:
            open_status = hours_div.first.inner_text().split('⋅')[0].strip()
            open_status = open_status.replace('\n', ' ')
        else:
            # Fallback
            for span in page.locator('span').all_inner_texts():
                if 'Open ' in span or 'Closed ' in span or 'Opens ' in span or 'Closes ' in span:
                    open_status = span.strip()
                    break



        return {
            "Business Name": name,
            "Rating": rating,
            "Review Count": reviews_count,
            "Category": category,
            "Address": address,
            "Phone Number": phone,
            "Website URL": website,
            "Open Status": open_status
        }
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def main():
    import sys
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
        
    parser = argparse.ArgumentParser(description="Google Maps Scraper")
    parser.add_argument("--city", help="City (شهر)", required=True)
    parser.add_argument("--category", help="Business Category (حوزه فعالیت)", required=True)
    args = parser.parse_args()
    
    query = f"{args.category} در {args.city}"
    search_url = f"https://www.google.com/maps/search/{urllib.parse.quote(query)}?hl=en"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()
        
        print(f"Searching for: {query}")
        page.goto(search_url, timeout=60000)
        
        try:
            page.wait_for_selector('a[href*="/maps/place/"]', timeout=20000)
        except:
            print("No results found or page took too long to load.")
            browser.close()
            return
            
        print("Scrolling through results to load all items...")
        
        last_count = 0
        retries = 0
        while True:
            items = page.locator('a[href*="/maps/place/"]')
            count = items.count()
            
            if count > 0:
                try:
                    items.nth(count - 1).hover()
                    page.mouse.wheel(0, 3000)
                except Exception:
                    pass
            
            time.sleep(2.5)
            new_count = page.locator('a[href*="/maps/place/"]').count()
            
            if new_count == last_count:
                retries += 1
                if retries > 3:
                    break
            else:
                retries = 0
                last_count = new_count
                
        items = page.locator('a[href*="/maps/place/"]')
        count = items.count()
        urls = []
        for i in range(count):
            href = items.nth(i).get_attribute('href')
            if href and href not in urls:
                urls.append(href)
                
        print(f"Found {len(urls)} listings. Starting extraction...")
        
        extracted_data = []
        for i, url in enumerate(urls, 1):
            print(f"Scraping [{i}/{len(urls)}]: {url}")
            data = extract_place_data(page, url)
            if data:
                extracted_data.append(data)
                
        browser.close()
        
    if not extracted_data:
        print("No data extracted.")
        return
        
    os.makedirs(".tmp", exist_ok=True)
    out_path = os.path.join(".tmp", "google_maps_directory_output.xlsx")
    df = pd.DataFrame(extracted_data)
    
    # Export and format with openpyxl
    with pd.ExcelWriter(out_path, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Listings')
        worksheet = writer.sheets['Listings']
        
        # Professional column formatting: adjusting widths dynamically
        for i, col in enumerate(df.columns):
            # Calculate column width based on max data length
            column_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
            column_len = min(column_len, 60) # Cap maximum width at 60 characters
            # Map index to Excel column letter (0->A, 1->B, ...)
            worksheet.column_dimensions[chr(65 + i)].width = column_len
    
    print("\n" + "="*50)
    print(f"Scraping Complete! Extracted {len(extracted_data)} records.")
    print(f"Data successfully formatted and saved to: {out_path}")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
