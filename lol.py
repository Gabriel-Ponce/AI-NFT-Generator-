import requests
from fake_useragent import FakeUserAgent

a = FakeUserAgent()

print('a', a.firefox)

headers = {'User-Agent': str(a.firefox)}

response = requests.get('https://api.opensea.io/api/v1/assets?format=json&include_orders=false&limit=20&order_direction=desc', headers= headers)

print(response)

with open('a.txt', 'w') as xd:

    xd.write(str(response.content))