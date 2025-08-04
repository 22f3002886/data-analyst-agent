import requests
import pandas as pd
from bs4 import BeautifulSoup

def scrape_wikipedia_table(task: str) -> pd.DataFrame:
    # Find the first URL in the task
    lines = task.split("\n")
    url = None
    for line in lines:
        if "wikipedia.org" in line:
            url = line.strip()
            break

    if not url:
        raise ValueError("No Wikipedia URL found in task.")

    # Download the page
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch page: {url}")

    # Parse HTML and extract table
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"class": "wikitable"})
    if not table:
        raise Exception("No wikitable found on the page.")

    # Convert to DataFrame
    df = pd.read_html(str(table))[0]
    return df