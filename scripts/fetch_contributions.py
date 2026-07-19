import requests
from bs4 import BeautifulSoup
import json
import os
import sys

# ---> REPLACE THIS WITH YOUR GITHUB USERNAME <---
USERNAME = "bismitw"

def fetch_data():
    url = f"https://github.com/users/{USERNAME}/contributions"
    print(f"Fetching data from {url}...")
    
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code}")
        sys.exit(1)

    # Parse the HTML to find the contribution boxes
    soup = BeautifulSoup(response.text, 'html.parser')
    days = soup.find_all("td", class_="ContributionCalendar-day")
    
    contributions = []
    for day in days:
        date = day.get('data-date')
        level = day.get('data-level')
        if date and level is not None:
            contributions.append({
                "date": date,
                "level": int(level)
            })
    
    if not contributions:
        print("Error: Could not find contribution data. Double check the username!")
        sys.exit(1)
        
    # Save the parsed data to a JSON file
    os.makedirs("data", exist_ok=True)
    with open("data/contributions.json", "w") as f:
        json.dump(contributions, f, indent=2)
    
    print(f"Success! Saved {len(contributions)} days of data to data/contributions.json")

if __name__ == "__main__":
    fetch_data()