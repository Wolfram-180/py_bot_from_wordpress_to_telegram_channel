import requests
import json
from bs4 import BeautifulSoup

import secrets

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}

url = 'https://www.' + secrets.site_url +  '/wp-json/wp/v2/posts'

response = requests.get(url , headers=header)
data = json.loads(response.text)

last_post = data[0]['id']

for curr_post in range(last_post - 10, last_post):
    url = 'https://www.' + secrets.site_url +  '/wp-json/wp/v2/posts?include[]=' + str(curr_post)
    response = requests.get(url , headers=header)
    data = json.loads(response.text)
    if len(data) > 0:
        id = data[0]['id']
        title = data[0]['title']['rendered']
        content = data[0]['content']['rendered']
        print(id)
        print(title)
        content = response.content
        soup = BeautifulSoup(content, "html.parser")
        for link in soup.find_all('a'):
            if 'uploads' in link.attrs['href']:
                dnld_lnk = link.attrs['href']
                print(link.get('href'))
            #for src in link.find_all('src'):
            #    print(src)
        #print(content)

#data = response.json()
#print(response)
#print(data)

#for item in data:
#    title = item['title']['rendered']
#    content = item['content']['rendered']
#    print(title)
#    print(content)

#content = r.content
#soup = BeautifulSoup(content, "html.parser")