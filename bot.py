import requests
import json
import base64

import secrets

url = 'https://www.' + secrets.site_url +  '/wp-json/wp/v2/posts/?filter[p]=1'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}
response = requests.get(url , headers=header)

#data = response.json()

data = json.loads(response.text)

#print(response)
#print(data)

for item in data:
    print(item['title']['rendered'])
    print(item['content']['rendered'])