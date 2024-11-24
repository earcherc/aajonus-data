import requests
from bs4 import BeautifulSoup
from pathlib import Path

def setup_data_directory():
    try:
        data_dir = Path(__file__).resolve().parent / "data"
    except NameError:
        data_dir = Path.cwd() / "data"
    data_dir.mkdir(exist_ok=True)
    return data_dir

def get_soup(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, "html.parser")
    return None

def extract_article_content(article_soup):
    content_div = article_soup.find("div", class_="content")
    if not content_div:
        return None
    
    paragraphs = content_div.find_all("p")
    return "\n\n".join(paragraph.text.strip() for paragraph in paragraphs)

def save_article(content, title, data_dir):
    filename = title.replace(" ", "_").replace("/", "_").replace('"', "") + ".txt"
    file_path = data_dir / filename
    file_path.write_text(content)
    print(f'Article "{title}" saved as {filename}.')

def scrape_articles(base_url):
    data_dir = setup_data_directory()
    soup = get_soup(base_url)
    if not soup:
        return
    
    articles = soup.find_all("div", class_="card-md")
    for article in articles:
        link_element = article.find("a", class_="read-more")
        if not link_element or not link_element.get("href"):
            continue
            
        article_url = base_url + link_element.get("href").lstrip("/")
        article_soup = get_soup(article_url)
        if not article_soup:
            continue
            
        content = extract_article_content(article_soup)
        if content:
            save_article(content, link_element.text.strip(), data_dir)

if __name__ == "__main__":
    scrape_articles("https://aajonus.net/")