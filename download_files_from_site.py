from time import sleep
import requests
import json
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse
from urllib import request
import re

import environment_params

'''

Purpose of that script: download data from WordPress posts to local folder

'''

### POSSIBLE ISSUE : Apache server-side issue: Mod_security may deny the download, in such case - disable mod_security on server side

# def get_filename_from_cd(cd) - not used, but may be useful
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

# start VVV
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}

# url like site.com
url = 'https://www.' + environment_params.site_url +  '/wp-json/wp/v2/posts'

response = requests.get(url , headers=header)
data = json.loads(response.text)

last_post = data[0]['id']

for curr_post in range(last_post - 10, last_post):
    url = 'https://www.' + environment_params.site_url +  '/wp-json/wp/v2/posts?include[]=' + str(curr_post)
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

                r = requests.get(full_fname, allow_redirects=True)
                open(file_name, 'wb').write(r.content)