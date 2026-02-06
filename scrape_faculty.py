import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# CONFIGURATION
URLS = [
    ("https://www.daiict.ac.in/faculty", "Faculty"),
    ("https://www.daiict.ac.in/adjunct-faculty", "Adjunct Faculty"),
    ("https://www.daiict.ac.in/distinguished-professor", "Distinguished Professor"),
    ("https://www.daiict.ac.in/professor-practice", "Professor of Practice"),
    ("https://www.daiict.ac.in/adjunct-faculty-international", "Adjunct Faculty International")
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Filtering out non-faculty rows just in case
IGNORE_LIST = ["contact us", "quick links", "menu", "search"]

def clean_text(text):
    if not text: return ""
    return re.sub(r'\s+', ' ', text).strip()

def parse_email(text):
    """Converts user[at]domain[dot]com to user@domain.com"""
    if not text: return "N/A"
    # Basic cleanup
    text = clean_text(text)
    # Replace obfuscation
    text = text.replace("[at]", "@").replace("[dot]", ".")
    return text

def scrape_daiict_csv():
    all_data = []
    print(f"{'Name':<30} | {'Email':<35} | {'Status'}")
    print("-" * 80)

    for url, category in URLS:
        try:
            print(f"Fetching {category}...")
            response = requests.get(url, headers=HEADERS, timeout=15)
            if response.status_code != 200:
                print(f"   -> Failed (Status {response.status_code})")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')

            # TARGETED SELECTOR: Only looks inside the faculty list container
            cards = soup.select('.facultyInformation ul li')

            if not cards:
                print(f"   -> No profiles found for {category}. Checking fallback selectors...")
                # Fallback in case specific page structure differs slightly
                cards = soup.select('.view-content .views-row')

            for card in cards:
                # 1. Extract Name
                name_tag = card.select_one('.personalDetails h3 a')
                if not name_tag:
                    # Try fallback for name
                    name_tag = card.select_one('h3')

                if not name_tag: continue
                name = clean_text(name_tag.get_text())

                # Filter Ignore List
                if any(ignored in name.lower() for ignored in IGNORE_LIST):
                    continue

                # 2. Extract Specific Fields
                education = "N/A"
                edu_tag = card.select_one('.facultyEducation')
                if edu_tag:
                    education = clean_text(edu_tag.get_text())

                email = "N/A"
                email_tag = card.select_one('.facultyemail')
                if email_tag:
                    email = parse_email(email_tag.get_text())

                phone = "N/A"
                phone_tag = card.select_one('.facultyNumber')
                if phone_tag:
                    phone = clean_text(phone_tag.get_text())

                interest = "N/A"
                interest_tag = card.select_one('.areaSpecialization')
                if interest_tag:
                    interest = clean_text(interest_tag.get_text())

                # 3. Extract Links
                profile_link = "N/A"
                if name_tag.name == 'a' and name_tag.has_attr('href'):
                      profile_link = name_tag['href']

                if profile_link != "N/A" and not profile_link.startswith("http"):
                    profile_link = "https://www.daiict.ac.in" + profile_link

                image_url = "N/A"
                img_tag = card.select_one('.facultyPhoto img')
                if img_tag and img_tag.has_attr('src'):
                    src = img_tag['src']
                    if not src.startswith("http"):
                        image_url = "https://www.daiict.ac.in" + src
                    else:
                        image_url = src

                # 4. Append Data
                all_data.append({
                    "Name": name,
                    "Designation": category,
                    "Email": email,
                    "Phone": phone,
                    "Education": education,
                    "Area_of_Interest": interest,
                    "Profile_Link": profile_link,
                    "Image_URL": image_url
                })

                print(f"{name[:25]:<30} | {email[:30]:<35} | OK")

        except Exception as e:
            print(f"Error scraping {url}: {e}")

    # SAVE TO CSV 
    if all_data:
        df = pd.DataFrame(all_data)
        # Final cleanup to ensure no duplicates
        df.drop_duplicates(subset=['Name', 'Email'], inplace=True)

        filename = "daiict_faculty_final.csv"
        df.to_csv(filename, index=False)
        print("\n" + "="*50)
        print(f"SUCCESS: Scraped {len(df)} profiles.")
        print(f"Data saved to: {filename}")
        print("="*50)
    else:
        print("No data found.")

if __name__ == "__main__":
    scrape_daiict_csv()