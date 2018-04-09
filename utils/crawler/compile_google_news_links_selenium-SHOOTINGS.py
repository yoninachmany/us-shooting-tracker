import sys
import urllib.request, urllib.error, urllib.parse
import urllib.request, urllib.parse, urllib.error
from http.cookiejar import CookieJar
import lxml.etree
import lxml.html
import re
from datetime import timedelta, date
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep
import random
import os
import pickle
import validators

from newspaper import Article, ArticleException

"""
This script was written to search Google news for a list of search terms over a
specified range of dates.  The idea here is to replicate the methodology used by
Jennifer Mascia to put together the The Gun Report, which was a New York Times blog
that chronicled daily shootings across the country.  The methodology is described
in an On the Media interview:  http://www.onthemedia.org/story/end-gun-report/
"""


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield end_date - timedelta(n)


if len(sys.argv) < 3:
    print("Usage: python compile_google_news_links_selenium-SHOOTINGS.py startYear-startMonth-startDay endYear-endMonth-endDay\n")
    exit(0)

sdate = sys.argv[1]
edate = sys.argv[2]
sy, sm, sd = sdate.split('-')
ey, em, ed = edate.split('-')
start_date = date(int(sy), int(sm), int(sd))
end_date = date(int(ey), int(em), int(ed))



search_terms = [ "man shot", "woman shot", "officer-involved shooting"]
blacklist = ['https://www.youtube.com/?gl=US', 'https://www.blogger.com/?tab=nj']

print("Search from %s to %s for terms %s\n"%(start_date, end_date, str(search_terms)))

def main():
    first_run = True
    driver = webdriver.Chrome('./chromedriver')
    crawl_output = {} # url -> dict representing article

    if os.path.exists('crawl_output.p'):
        crawl_output = pickle.load(open('crawl_output.p', 'rb'))

    i = 0

    # Iterate through dates
    for single_date in daterange(start_date, end_date):
        for term in search_terms:
            url = 'https://www.google.com/search?'
            values = {'q' : term,
              'hl' : 'en',
              'gl' : 'us',
              'authuser' : '0',
              'source' : 'lnt',
              'tbs' : 'cdr:1,cd_min:' + single_date.strftime("%m/%d/%Y") + ",cd_max:" + single_date.strftime("%m/%d/%Y"),
              'tbm' : 'nws',
              'start' : '0' }

            print("***" + url + urllib.parse.urlencode(values))
            driver.get(url + urllib.parse.urlencode(values))
            if first_run:
                print("Set search preferences by going to Settings > Search Settings, and selecting 'Never show instant results', and then set the Results per page to ***40***")
                sleep(60)
                first_run = False
            for i,a in enumerate(driver.find_elements_by_tag_name('a')):
                try:
                    link = a.get_attribute('href')
                    while link is not None and link.startswith('https://ipv4.google.com/sorry/'): #captchas
                        print("Blocked on: %s\n"%(str(link)))
                        sleep(10)
                        link = a.get_attribute('href')

                    if link is not None and link not in crawl_output.keys() and validators.url(link) and link not in blacklist:
                        if "google.com" not in link and "webcache.googleusercontent" not in link: #remove some obvious ads and junk <a> elements
                            print(single_date)
                            print(single_date.strftime("%Y-%m-%d"), "\t", term, "\t", end=' ')
                            print(link)

                            try:
                                article = Article(link)
                                article.download()
                                article.parse()

                                pub_date = article.publish_date
                                text = article.text
                                title = article.title

                                if pub_date is None or text is None or title is None:
                                    continue

                                article_dict = {
                                    'publication data': str(pub_date),
                                    'text': str(text),
                                    'title': str(title),
                                }

                                crawl_output[link] = article_dict

                                i += 1
                                if i % 30 == 0:
                                    # every 30 articles, dump the output
                                    print('dumping crawl_output')
                                    pickle.dump(crawl_output, open('crawl_output.p', 'wb'))

                            except ArticleException:
                                # invalid article
                                continue


                except StaleElementReferenceException:
                    print("Stale element: %s\n"%str(a))

    driver.close()

    print('dumping crawl_output')
    print('{} articles crawled'.format())
    pickle.dump(crawl_output, open('crawl_output.p', 'wb'))


if __name__ == "__main__":
    main()
