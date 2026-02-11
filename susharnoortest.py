import requests
import csv
import os
import pyperclip
import datetime

from query_responder import GeminiOperator
from scraping_tools import get_text_from_url

# --- CONFIGURATION ---
API_KEY = os.getenv('SEARCH_API_KEY')
CX = "44239356eba9f4164"
QUERY = "volunteer events California March 2026"
NUM_RESULTS = 10
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
CSV_FILE = f"volunteer_links_api_{timestamp}.csv"

newOperator = GeminiOperator()
results = []

start_index = 1

# --- CSV FIELDS ---
FIELDNAMES = [
    "event_title",
    "name_of_organization",
    "additional_info",
    "image_link",
    "alt_image_link",
    "link",
    "where",
    "start_time",
    "end_time",
    "date",
    "one_time",
    "days",
    "other_filters",
    "passion_areas",
    "time_of_day"
]

# ✅ OPEN CSV FILE AT THE START
csv_file = open(CSV_FILE, "w", newline="", encoding="utf-8")
writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
writer.writeheader()
csv_file.flush()  # Save header immediately
print(f"📄 Created {CSV_FILE}")

# --- SEARCH LOOP ---
try:
    while len(results) < NUM_RESULTS:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": API_KEY,
            "cx": CX,
            "q": QUERY,
            "start": start_index,
            "num": min(10, NUM_RESULTS - len(results))
        }

        print(f"\n🔍 Fetching batch starting at index {start_index}...")
        response = requests.get(url, params=params, timeout=10).json()
        items = response.get("items", [])

        if not items:
            print("No more results found.")
            break

        print(f"Found {len(items)} search results in this batch")

        for idx, item in enumerate(items, 1):
            if len(results) >= NUM_RESULTS:
                break

            link = item.get("link")
            if not link:
                continue

            print(f"\n[{len(results)}/{NUM_RESULTS}] Processing result {idx}/{len(items)}: {link[:60]}...")

            # --- SCRAPE PAGE ---
            try:
                full_text = get_text_from_url(link, timeout=10)

                if "Error fetching" in full_text or "404" in full_text:
                    print(f"⏭️  Skipped: Page unreachable")
                    continue

            except Exception as e:
                print(f"❌ Scraping failed: {type(e).__name__}")
                continue

            # --- GET FULL JSON FIELDS FROM GEMINI ---
            try:
                json_block = newOperator.answer_onetime_json_query(full_text)
                json_dict = json_block.model_dump()
                json_dict["link"] = link

                print(f"   one_time: '{json_dict.get('one_time')}'")

                if json_dict.get("one_time", "").lower() == 'yes':
                    results.append(json_dict)

                    # ✅ WRITE ROW IMMEDIATELY
                    writer.writerow(json_dict)
                    csv_file.flush()  # Force write to disk

                    print(f"✅ Valid event: {json_dict['event_title']}")
                    print(f"   💾 Saved to CSV (row {len(results)})")
                else:
                    print(f"⏭️  Skipped: Not a one-time event")

            except Exception as e:
                print(f"❌ JSON extraction failed: {type(e).__name__}: {str(e)[:100]}")
                continue

        # Increment start_index to avoid infinite loop
        start_index += len(items)

finally:
    # ✅ CLOSE FILE WHEN DONE (or if script crashes)
    csv_file.close()
    print(f"\n📄 CSV file closed: {CSV_FILE}")

# --- COPY TO CLIPBOARD ---
csv_string = ",".join(FIELDNAMES) + "\n"
for r in results:
    row = [str(r.get(field, "")) for field in FIELDNAMES]
    csv_string += ",".join(row) + "\n"

pyperclip.copy(csv_string)

print(f"\n✅ Extracted {len(results)} rows")
print(f"📋 CSV copied to clipboard!")
print(f"📄 Saved to {CSV_FILE}")