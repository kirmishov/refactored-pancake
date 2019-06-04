import logging

from bs4 import BeautifulSoup
from selenium import webdriver

from models import AdStruct


logging.basicConfig(filename='taboola.log',format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)


class TaboolaScraper():

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.driver = webdriver.Chrome(options=self.options)
    
    def scrape_page(self, url):
        self.driver.get(url)
        logging.info('URL: {}'.format(url))
        
        # if page need to scroll down for displaying ads,
        # we can improve script
        """
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(1)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        """
        
        logging.info('Title page: {}'.format(self.driver.title))
        html_content = self.driver.page_source
        html_file = open("{}.html".format(self.driver.title), "w")
        html_file.write(html_content)
        html_file.close()
        soup = BeautifulSoup(html_content, "html.parser")
        ad_divs_taboola = soup.select('div[class*="videoCube trc_spotlight_item origin-default thumbnail_top"]')
        
        if len(ad_divs_taboola)>0:
            logging.info('Number of Taboola ads found: {}'.format(len(ad_divs_taboola)))
            for ad_div in ad_divs_taboola:
                ad = AdStruct()
                ad.network_name = 'Taboola'
                if ad_div.findNext('a'):
                    ad.title = ad_div.findNext('a')['title']
                    ad.dest_link = ad_div.findNext('a')['href']
                    logging.info('Ad title: {}'.format(ad.title))
                    logging.info('Dest link: {}'.format(ad.dest_link))
                if ad_div.findNext('span'):
                    ad.image_url = ad_div.findNext('span')['style'].split('url("')[1].split('");')[0]
                    logging.info('Ad image: {}'.format(ad.image_url))
                if ad_div.findNext('span', {'class': 'branding'}):
                    ad.text =  ad_div.findNext('span', {'class': 'branding'}).text
                    logging.info('Ad text: {}'.format(ad.text))

                # call API here to send data
        
        else:
            logging.warning('0 ads found')

    
    def quit(self):
        self.driver.quit()


urls = [
    'https://www.bild.de/',
    'https://www.bild.de/unterhaltung/leute/leute/meier-casiraghi-sayn-wittgenstein-ein-wochenende-drei-traumhochzeiten-62352346.bild.html',
    'https://www.nbcnews.com/',
    'https://www.nbcnews.com/news/us-news/kevin-hassett-top-white-house-economic-adviser-leaving-trump-says-n1012996',
    'https://www.foxnews.com/',
    'https://www.dailymail.co.uk/femail/article-7098355/Melania-Trump-pays-tribute-D-Day-veterans-military-themed-650-Burberry-blouse.html',
]


if __name__ == "__main__":
    scraper = TaboolaScraper()
    
    for url in urls:
        scraper.scrape_page(url)
    
    scraper.quit()
