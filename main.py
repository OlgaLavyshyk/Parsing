import requests
from bs4 import BeautifulSoup
import csv

CSV = 'currency.csv'
HOST = "https://www.nbrb.by/"
URL = "https://www.nbrb.by/statistics/rates/ratesmonth.asp"

HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}
def get_html(url, params =None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r
# html = get_html(URL)
# print(html)

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')

    currency = []
    # print(items)
# html = get_html(URL)
# get_content(html.text)
    data = []
    table = soup.find('table', attrs={'class': 'currencyTable'})
    table_body = table.find('tbody')

    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        currency.append(
            {
                'curName':row.find('td', class_='curName').get_text(strip=True),
                'curAmount':row.find('td', class_ ='cuыrAmount').get_text(strip=True),
                'curCours align-right':row.find('td', class_='curCours').get_text()

            }
        )
    return currency
html = get_html(URL)
print(get_content(html.text))

def save_doc(rows, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Наименование иностранной валюты', 'Буквенный код валюты', 'Официальный курс'])
        for row in rows:
            writer.writerow([row['curName'], row['curAmount'], row['curCours align-right'] ])

def parser():

    html = get_html(URL)
    if html.status_code == 200:
        currency = []
        currency = get_content(html.text)
        save_doc(currency, CSV)

    else:
        print('Error')

parser()

