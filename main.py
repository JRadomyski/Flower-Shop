import os
import requests
from bs4 import BeautifulSoup
import csv

def scrape_content(xml_url):
    contents = []

    try:
        response = requests.get(xml_url, timeout=5)
        if response.status_code != 200:
            print(f"Nie udało się załadować danych z: {xml_url}")
            return contents

        soup = BeautifulSoup(response.content, 'lxml-xml')
        articles = soup.find_all('item')

        for article in articles:
            link = article.find('link').get_text(strip=True)
            title = article.find('title').get_text(strip=True)
            image_link = article.find('g:image_link').get_text(strip=True) if article.find('g:image_link') else 'Brak'
            custom_label_1 = article.find('g:custom_label_1').get_text(strip=True) if article.find('g:custom_label_1') else 'Brak'

            contents.append((link, title, image_link, custom_label_1))

    except requests.RequestException as e:
        print(f"Błąd podczas łączenia z adresem: {xml_url} - {e}")

    return contents


def save_to_csv(contents, filename):
    if not os.path.exists('outputs'):
        os.makedirs('outputs')

    path = os.path.join('outputs', filename)
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Link', 'Title', 'Image Link', 'Custom Label 1'])
        for content in contents:
            writer.writerow(content)

xml_url = "https://newsletter.onet.pl/api/feed.xml"
filename = "articles.csv"

contents = scrape_content(xml_url)
save_to_csv(contents, filename)

print(f"Zakończono zapisywanie treści do folderu 'outputs' w pliku {filename}")


# <g:custom_label_1> personalizacja_kategoria_wiadomosci </g:custom_label_1>