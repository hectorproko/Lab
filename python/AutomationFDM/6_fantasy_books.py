import requests
from bs4 import BeautifulSoup

def get_one_star_fantasy_books():
    base_url = "http://books.toscrape.com/catalogue/category/books/fantasy_19/"
    books = []
    page_url = "index.html"
    
    while page_url:
        # Fetch the page
        try:
            response = requests.get(base_url + page_url)
            response.raise_for_status()  # Raise exception for bad status codes
        except requests.RequestException as e:
            print(f"Error fetching page {page_url}: {e}")
            break
        
        # Parse the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all book articles
        book_articles = soup.find_all('article', class_='product_pod')
        for article in book_articles:
            # Check for 1-star rating
            rating = article.find('p', class_='star-rating')
            if rating and 'One' in rating.get('class', []):
                # Extract title
                title_tag = article.find('h3').find('a')
                if title_tag:
                    title = title_tag.get('title', '').strip()
                    if title:
                        books.append(title)
        
        # Check for next page
        next_button = soup.find('li', class_='next')
        page_url = next_button.find('a')['href'] if next_button and next_button.find('a') else None
    
    return books

def main():
    one_star_books = get_one_star_fantasy_books()
    for book in one_star_books:
        print(book)

if __name__ == "__main__":
    main()