from bs4 import BeautifulSoup
import requests
import argparse
import json
from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO


def load_image_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error for bad status codes
        return Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

url = "https://news.google.com/home?hl=en-IN&gl=IN&ceid=IN:en"
target_url = "https://news.google.com"
response = requests.get(url)

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
DEFAULT_CONFIG = {
    "base_url": "https://news.google.com",
    "output_file": "news_data.json",
    "selectors": {
        "article": "article[class*='IBr9hb']",
        "title": "a[class*='gPFEn']",
        "source": "div[class*='vr1PYe']",
        "image": "img[class*='Quavad']",
        "thumbnail": {
            "container": "figure[class*='K0q4G']",  # Thumbnail container
            "img": "img[class*='Quavad']",         # Actual image element
            "fallback": "div[class*='DwnlN']"      # Background 
        },
        "time": "time"
    }
}
try:
    response = requests.get(DEFAULT_CONFIG["base_url"], headers=headers)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")


soup = BeautifulSoup(response.content, 'html.parser')
news_items = []

for article in soup.select(DEFAULT_CONFIG["selectors"]["article"]):
    item = {}
    if title_elem := article.select_one(DEFAULT_CONFIG["selectors"]["title"]):
        item["title"] = title_elem.text
        # item["link"] = urljoin(DEFAULT_CONFIG["base_url"], title_elem.get('href'))

    if img_elem := article.select_one(DEFAULT_CONFIG["selectors"]["image"]):
    # Try multiple possible attributes for image URL
        item["image"] = (
            target_url + img_elem.get('srcset').split()[0]           # Standard attribute
            # img_elem.get('data-src') or     # Lazy-loaded images
            # img_elem.get('data-iurl')       # Google-specific CDN URLs
        )
        img = load_image_from_url(item["image"])
        if img:
            img.show()  # Display the image
    
    if source_elem := article.select_one(DEFAULT_CONFIG["selectors"]["source"]):
        item["source"] = source_elem.text
    
    if time_elem := article.select_one(DEFAULT_CONFIG["selectors"]["time"]):
        item["timestamp"] = time_elem.get('datetime')
    
    if item:
        news_items.append(item)
print(news_items)
