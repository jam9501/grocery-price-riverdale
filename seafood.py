import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

url = "https://www.foodtown.com/shopping#!/?department_id=440"

def scrape_products():

    response = requests.get(url)
    response.raise_for_status()  # Check for request errors

    soup = BeautifulSoup(response.text, 'html.parser')

    product_list = soup.find('ul', class_='fp-result-list fp-product-list fp-product-list-lg')

    products = []

    for item in product_list.find_all('li', class_='fp-item'):
        name = item.find('div', class_='fp-item-name notranslate').get_text(strip=True)
        sale_price = item.find('strong').get_text(strip=True)
        original_price = item.find('span', class_='fp-item-base-price').get_text(strip=True)
        size = item.find('span', class_='fp-item-size').get_text(strip=True)
        
        extraction_date = datetime.now().strftime('%Y-%m-%d')

        products.append({
            'Product Name': name,
            'Sale Price': sale_price,
            'Original Price': original_price,
            'Size/Weight': size,
            'Extraction Date': extraction_date
        })

    df = pd.DataFrame(products)

    df.to_csv('products.csv', index=False)

if __name__ == '__main__':
    scrape_products()
