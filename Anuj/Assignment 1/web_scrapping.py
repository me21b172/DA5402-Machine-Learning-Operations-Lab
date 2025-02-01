from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
import requests
import ast
from concurrent.futures import ThreadPoolExecutor

def read_text_file():
    with open("Anuj/Assignment 1/config_file.txt", "r") as file:
        return ast.literal_eval(file.read())

def download_and_process_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        image = response.content
        return image
    except Exception as e:
        print(f"Error processing image from {url}: {e}")
        return None
    

def extract_top_stories():
    DEFAULT_CONFIG = read_text_file()
    try:
        response = requests.get(DEFAULT_CONFIG["url"], headers=DEFAULT_CONFIG["headers"])
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")


    soup = BeautifulSoup(response.content, 'html.parser')
    link = DEFAULT_CONFIG["target_url"] + soup.find("a",class_="aqvwYd").get('href')
    try:
        response = requests.get(
            link, 
            headers=DEFAULT_CONFIG["headers"],
            params=DEFAULT_CONFIG["params"],
            timeout=100,
            allow_redirects=True,
            stream=True
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")


    soup = BeautifulSoup(response.content, 'html.parser')
    news_items = []

    for article in soup.select(DEFAULT_CONFIG["selectors"]["article"]):
        item = {}
        link_elem = article.select_one(DEFAULT_CONFIG["selectors"]["link"])
        title_elem = article.select_one(DEFAULT_CONFIG["selectors"]["title"])
        img_elem = article.select_one(DEFAULT_CONFIG["selectors"]["image"])
        source_elem = article.select_one(DEFAULT_CONFIG["selectors"]["source"])
        time_elem = article.select_one(DEFAULT_CONFIG["selectors"]["time"])
        if link_elem is not None and title_elem is not None and img_elem is not None and source_elem is not None and time_elem is not None:
            item["link"] =  DEFAULT_CONFIG["target_url"] +  link_elem.get('href')
            item["title"] = title_elem.text
            item["image"] = DEFAULT_CONFIG["target_url"] + img_elem.get('srcset').split()[0]           # Standard attribute
            item["source"] = source_elem.text
            item["timestamp"] = time_elem.get('datetime')
        
        if item:
            news_items.append(item)
    # Extracting Image and parallelising the to load he image
    image_url = [news["image"] for news in news_items ] 
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(download_and_process_image, image_url))
    for i,news in enumerate(news_items):
        news["image"] = results[i]
    return news_items
if __name__ == "__main__":
    print(len(extract_top_stories()))
# print(len(extract_top_stories()))
