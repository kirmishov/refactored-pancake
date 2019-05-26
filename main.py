import json

from bs4 import BeautifulSoup
from selenium import webdriver

from models import AdStruct

url = 'https://www.welt.de/wirtschaft/plus193053737/Wolfgang-Reitzle-Das-Land-hat-keinen-Anspruch-mehr-an-sich-selbst.html'
ad_list = []


def get_webdriver(url, headless = False):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)
    # print (driver.title)
    return driver


driver = get_webdriver(url)
html_content = driver.page_source

soup = BeautifulSoup(html_content, "html.parser")
driver.quit()

"""
# save to file
html_file = open("filename.html", "w")
html_file.write(html_content)
html_file.close()
"""

for block in soup.find_all('div', {'data-component': 'TaboolaComponent'}):
    ad = AdStruct()
    ad.network_name = 'Taboola'
    for ad_div in block.find_all('div', {'data-item-syndicated': 'true'}):
        if ad_div.findNext('a'):
            ad.title = ad_div.findNext('a')['title']
            ad.dest_link = ad_div.findNext('a')['href']
        if ad_div.findNext('span'):
            ad.image_url = ad_div.findNext('span')['style'].split('url("')[1].split('");')[0]
            # sure better use regex
        if ad_div.findNext('span', {'class': 'branding'}):
            ad.text =  ad_div.findNext('span', {'class': 'branding'}).text
        
        ad_list.append({
            'network_name': ad.network_name,
            'title': ad.title,
            'dest_link': ad.dest_link,
            'image': ad.image_url,
            'text': ad.text
        })


with open('output.json', 'w') as fp:
    json.dump(ad_list, fp, indent=4, ensure_ascii=False)
fp.close()
