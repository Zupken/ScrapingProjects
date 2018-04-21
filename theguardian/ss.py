import scraper as sc
import lxml.html
import requests


class Scraping:

    def __init__(self):
        self.site = 'https://www.theguardian.com/film+tone/reviews?page='
        self.links = []
        self.data = []

    def get_links(self):
        for number in range(1, 866):
            source = requests.get(self.site+str(number))
            tree = lxml.html.fromstring(source.content)
            etree = tree.xpath('//div[@class="fc-item__container"]')
            for element in etree:
                link = sc.get_href(element.xpath('./theguardian[@href]'))
                self.links += link
            print('Site number: '+str(number))

    def get_data(self):
        for link in self.links:
            source = requests.get(link)
            tree = lxml.html.fromstring(source.content)
            headline = sc.get_text(tree.xpath('//h1[contains(@class, "headline")]/text()'))
            rating = tree.xpath('count(//div[@class="u-cf"]//span[contains(@class, "golden")])')
            description = sc.get_text(tree.xpath('//div[@class="content__standfirst"]/p/text()'))
            print(self.links.index(link)+1, 'from: ', len(self.links))
            if description == 'N/D':
                description = sc.get_text(tree.xpath('//div[@class="content__standfirst"]//text()'))
            review = sc.get_text(tree.xpath('//div[contains(@class, "article-body")]/p[1]//text()'))
            self.data.append([link, headline, rating, description, review])
        sc.Excel(('link', 'headline', 'rating', 'description', 'review')).excel(self.data)


Scraping = Scraping()
Scraping.get_links()
Scraping.get_data()
