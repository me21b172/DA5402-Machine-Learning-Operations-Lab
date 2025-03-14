import requests
import ast

def read_text_file():
    '''Reading config file'''

    with open("config_file.txt", "r") as file:      # Change the file location depeding on it's location
        return ast.literal_eval(file.read())
    
def factoring_lazy_loading(link):
    '''Factoring lazy loading'''

    DEFAULT_CONFIG = read_text_file()
    response = requests.get(
                link, 
                headers=DEFAULT_CONFIG["headers"],
                params=DEFAULT_CONFIG["params"],    #Module 3 To incorporate Lazy loading (look into params into config file for more inf)
                timeout=100,
                allow_redirects=True,
                stream=True
            )
    return response


def extract_news_meta_data(article):
    '''Extracting news meta data'''

    DEFAULT_CONFIG = read_text_file()
    link_elem = article.select_one(DEFAULT_CONFIG["selectors"]["link"])
    title_elem = article.select_one(DEFAULT_CONFIG["selectors"]["title"])
    img_elem = article.select_one(DEFAULT_CONFIG["selectors"]["image"])
    source_elem = article.select_one(DEFAULT_CONFIG["selectors"]["source"])
    time_elem = article.select_one(DEFAULT_CONFIG["selectors"]["time"])
    return link_elem, title_elem, img_elem, source_elem, time_elem
    

def download_and_process_image(url):
    '''Loading image from the url'''
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        image = response.content
        return image
    except Exception as e:
        print(f"Error processing image from {url}: {e}")
        return None