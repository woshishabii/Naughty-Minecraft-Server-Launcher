import requests
from bs4 import BeautifulSoup
import lxml

vanilla_source_url = 'https://getbukkit.org/download/vanilla'

vanilla_requests = requests.get(vanilla_source_url)

print(vanilla_requests)

vanilla_html_data = vanilla_requests.text

vanilla_soup = BeautifulSoup(vanilla_html_data, 'html.parser')

vanilla_links = []

for link in vanilla_soup.find_all('a'):
    # vanilla_links.append(link.get('href'))
    if link.get('href').startswith('https://getbukkit.org/get/'):
        vanilla_links.append(link.get('href'))

vanilla_download_links = []

# Analysis links like https://getbukkit.org/get/c503fcf07fdff1ffb5296f656c3c7a09
# To https://launcher.mojang.com/v1/objects/c503fcf07fdff1ffb5296f656c3c7a09/server.jar

for temp in vanilla_links:
    vanilla_download_links.append(f'https://launcher.mojang.com/v1/objects/{temp[26:]}/server.jar')

with open('text.txt', mode='w') as f:
    f.writelines(vanilla_download_links)






'''
for link in vanilla_links:
    data = requests.get(link)
    print(data.text)
    soup = BeautifulSoup(data.text, 'html.parser')
    for temp in soup.find_all('a'):
        if temp.startswith('https://launcher.mojang.com/v1/objects/'):
            vanilla_download_links.append(temp)
'''

'''
with open('text.html', mode='w') as f:
    f.write(vanilla_html_data.text)
'''