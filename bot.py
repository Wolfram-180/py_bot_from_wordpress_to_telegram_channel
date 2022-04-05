from time import sleep
import requests
import json
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse
from urllib import request
#from tqdm import tqdm
import re

import secrets

def get_filename_from_cd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]

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
                full_fname = urlparse(dnld_lnk)
                full_fname = (full_fname.path).replace('\\', '')
                full_fname = (full_fname).replace('"', '')
                full_fname = (full_fname).replace("'", "")
                #full_fname = (full_fname).replace("https://", "http://")
                
                file_name = os.path.basename(full_fname)

                #r = requests.get(full_fname, allow_redirects=True)
                open(file_name, 'wb').write(r.content)

                #print(download_file(full_fname))

                #wget.download(full_fname, file_name)

                #data = requests.get(full_fname)
                #with open(file_name, 'wb') as file:
                #    file.write(data.content)
                #    sleep(5)
                                
                #request.urlretrieve(full_fname, file_name)
                
                #resp_file = requests.get(full_fname, stream=True)
                #with open(file_name, "wb") as handle:
                #    for data in tqdm(response.iter_content()):
                #        handle.write(data)
                
                #_file = urllib.request.urlopen(full_fname)
                #with open(file_name,'wb') as output:
                #    output.write(_file.read())
                
                #print(full_fname) 
                #print(file_name)
                #resp_file = requests.get(full_fname, headers=header)
                #open(file_name, 'wb').write(resp_file.content)

