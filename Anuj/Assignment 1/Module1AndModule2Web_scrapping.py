#Run the code to get the top news from the website (Not really the main function which orchestrate all the modules)
from bs4 import BeautifulSoup
import requests
import ast
from concurrent.futures import ThreadPoolExecutor
from Module3 import factoring_lazy_loading,download_and_process_image,extract_news_meta_data,read_text_file

# Module 1 and Module 2
# Create a Python script using any web scrapping libraries to scrape the home page of Google News and Top Stories” link from the home page
def extract_top_stories():
    '''Workhorse for web scrapping'''

    DEFAULT_CONFIG = read_text_file()
    try:
        response = requests.get(DEFAULT_CONFIG["url"], headers=DEFAULT_CONFIG["headers"])
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

    soup = BeautifulSoup(response.content, 'html.parser')
    link = DEFAULT_CONFIG["target_url"] + soup.find("a",class_="aqvwYd").get('href')
    try:
        response = factoring_lazy_loading(link)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")


    soup = BeautifulSoup(response.content, 'html.parser')
    news_items = []

    # Going through the articles
    for article in soup.select(DEFAULT_CONFIG["selectors"]["article"]):
        item = {}
        link_elem, title_elem, img_elem, source_elem, time_elem = extract_news_meta_data(article)
        if link_elem is not None and title_elem is not None and img_elem is not None and source_elem is not None and time_elem is not None:
            item["link"] =  DEFAULT_CONFIG["target_url"] +  link_elem.get('href')
            item["title"] = title_elem.text
            item["image"] = DEFAULT_CONFIG["target_url"] + img_elem.get('srcset').split()[0]        
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
