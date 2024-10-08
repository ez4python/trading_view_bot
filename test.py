# from bs4 import BeautifulSoup
# import requests
#
#
# def get_response(url):
#     html_doc = requests.get(url).text
#     return html_doc
#
#
# link = "https://www.investing.com/earnings-calendar/"
#
# if __name__ == '__main__':
#     data = get_response(link)
#     soup = BeautifulSoup(data, 'html.parser')
#     print(soup.find('table', id='earningsCalendarData'))


import http.client

conn = http.client.HTTPSConnection("investing4.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "1a62f96e8fmsh146cb3db8ae2356p186756jsn5a268c3baa9b",
    'x-rapidapi-host': "investing4.p.rapidapi.com"
}

conn.request("GET", "/calendar/earnings-calendar", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
