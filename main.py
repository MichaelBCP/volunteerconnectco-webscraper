import csv
from scraping_tools import get_text_from_url, get_img_from_url
from query_responder import GeminiOperator

# Input and output files
input_csv = "C:\\Users\\mikeg\\Downloads\\volunteer_links_api.csv"
output_csv = "volunteer_output.csv"

newOperator = GeminiOperator()

# Read links from CSV
links = []
with open(input_csv, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        links.append(row['link'])  # second column named "link"

def clean(t):
    """Clean newlines and extra spaces"""
    return t.replace('\n', ' ').replace('\r', ' ').strip()


# Open output CSV for writing
with open(output_csv, 'w', newline='', encoding='utf-8') as f_out:
    writer = csv.writer(f_out)
    
    # Write header row
    writer.writerow([
        "Organization Name", "Volunteer Title", "URL", "Image", "Position Date", 
        "Description", "Age Requirement", "Skill Requirements", "Address/Virtual",
        "Passion Areas", "Specific Skills", "Filters"
    ])
    
    # Process each URL
    for url in links:
        print(f"Processing {url} ...")
        full_text = get_text_from_url(url)

        info = newOperator.answer_json_query(full_text)

        row = [info.name_of_organization, info.opportunity_title, url,
               "placeholder", info.position_date_start_end, info.description,
               info.age_requirement, info.experience_needed, info.locations,
               info.passion_areas, info.specific_skills]
        
        # Clean each cell
        row = [clean(cell) for cell in row]
        
        # Write row to CSV
        writer.writerow(row)
        print("✅ Row saved")

print(f"All data saved to {output_csv}")