from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_1?ie=UTF8&pg='
data_list = list()
pages_list = ['1', '2']

# scraping for information
for page in pages_list:

    param_dict = {
        'start': page
    }
    print(param_dict)

    html_link = requests.get(url + page).text
    soup = BeautifulSoup(html_link, 'lxml')

    book_card = soup.find_all('li', class_='zg-item-immersion')
    for index, book in enumerate(book_card):
        data_dict = dict()

        data_dict['rank'] = book.find('span', class_='zg-badge-text').text.strip()
        # Scraping Name of book
        try:
            data_dict['name'] = book.find('a', class_='a-link-normal').text.strip()
        except:
            data_dict['name'] = 'Not Available'

        # scraping author
        try:
            data_dict['author'] = book.find('div', class_='a-row a-size-small').text.strip()
        except:
            data_dict['author'] = 'Not Available'

        # scraping price of book
        try:
            data_dict['price'] = book.find('span', class_="p13n-sc-price").text.strip()[2:]
        except:
            data_dict['price'] = 'Not Available'

        # scraping type of book
        try:
            data_dict['book_type'] = book.find('span', class_='a-size-small a-color-secondary').text.strip()
        except:
            data_dict['book_type'] = 'Not Available'

        # scraping Stars
        try:
            data_dict['stars'] = str(book.find('span', class_='a-icon-alt').text.strip())
        except:
            data_dict['stars'] = 'Not Available'

        # scraping number of reviews
        try:
            data_dict['reviews'] = book.find('a', class_='a-size-small a-link-normal').text.strip()
        except:
            data_dict['reviews'] = 'Not Available'

        # link of book
        try:
            data_dict['link'] = 'https://www.amazon.in' + book.find('a', class_='a-link-normal')['href']
        except:
            data_dict['link'] = 'Not Available'

        data_list.append(data_dict)
        

# creating a DataFrame and adding scraped info to it
df = pd.DataFrame(data_list)
# exporting to csv
df.to_csv('amazon_bestsellers.csv', encoding='utf-8')
