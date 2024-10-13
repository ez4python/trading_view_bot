import cloudscraper
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper()

url = 'https://www.investing.com/earnings-calendar/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.3'
}

response = scraper.get(url, headers=headers)


def extract_earnings_info():
    soup = BeautifulSoup(response.text, 'html.parser')
    earnings_data = []
    table = soup.find('table', id="earningsCalendarData")
    table_rows = table.find_all('tr')[2:]

    for row in table_rows:
        data = {}
        span = row.find('span')
        if span:
            data.update({
                'country': span.get('title'),
            })
            if row.find('td').find('span'):
                # stock-title
                title = row.find('td', {'class': 'left noWrap earnCalCompany'}).text
                title = title.replace('\n', '').replace('\xa0', '')

                # stock-link
                stock_link = row.find('a', {'class': 'bold middle'}).get('href')

                # stock-actual
                stock_actual = row.find_all('td', {'class': 'leftStrong'})
                stock_eps = stock_actual[0].text.replace('/', '').replace('\xa0', '')
                stock_rev = stock_actual[1].text.replace('/', '').replace('\xa0', '')

                # stock-market-cap
                stock_market_cap = row.find('td', {'class': 'right'}).text

                data.update({
                    'title': title,
                    'stockLink': 'https://investing.com' + stock_link,
                    'stockEPS': stock_eps,
                    'stockREV': stock_rev,
                    'stockMarketCap': stock_market_cap
                })
        else:
            data.update({
                'theDay': row.find('td', {'class': 'theDay'}).text,
            })
        earnings_data.append(data)

    # data recycling
    new_data = []
    stock_data = extract_earnings_info()
    indexes = []
    for stock in stock_data:
        if stock.get('theDay'):
            indexes.append(stock_data.index(stock))
    for i in range(len(indexes)):
        if i < len(indexes) - 1:
            new_data.append(
                {
                    'date': stock_data[indexes[i]]['theDay'],
                    'quantity': len(stock_data[indexes[i] + 1:indexes[i + 1]]),
                    'stocks': stock_data[indexes[i] + 1:indexes[i + 1]]
                }
            )
        else:
            new_data.append(
                {
                    'date': stock_data[indexes[i]]['theDay'],
                    'quantity': len(stock_data[indexes[i] + 1:]),
                    'stocks': stock_data[indexes[i] + 1:]
                }
            )

    return new_data
