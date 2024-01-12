import subprocess
import json
import time
from bs4 import BeautifulSoup
from requests import get
from selenium import webdriver
from selenium.webdriver.common.by import By
# from openai import OpenAI
# client = OpenAI()

def read_article(link):
    completelink = 'https://www.tradingview.com' + link
    article_txt = get(completelink).text
    return article_txt

def write_article_to_file(article_txt, filename):
    with open(filename, 'w') as f:
        f.write(article_txt)

def call_js_script(filename):
    subprocess.run(['node', 'readermode.js', filename], check=True)

def get_last_news(html_text, lastnews, allnews):
    soup = BeautifulSoup(html_text, 'lxml')
    news = soup.find_all('a', class_="card-rY32JioV card-pDWUWIxC")
    lastnews = []
    for article in news:
        if article['href'] not in allnews:
            lastnews.append(article['href'])
            allnews.append(article['href'])
    return allnews

def get_news():
    driver = webdriver.Chrome()
    driver.get('https://www.tradingview.com/news/markets/')

    time.sleep(3)
    try:
        refreshbutton = driver.find_element(By.CLASS_NAME,
        "round-button-FujgyDpN color-black-FujgyDpN variant-primary-FujgyDpN size-medium-FujgyDpN with-start-icon-FujgyDpN")
        refreshbutton.click()
    except:
        print("no refresh button found")
    time.sleep(3)

    html_text = driver.page_source
    allnews = get_last_news(html_text, [])
    lastnews = []
    while (True):
        driver.refresh()
        time.sleep(3)
        html_text = driver.page_source
        try:
            refreshbutton = driver.find_element(By.XPATH,"//button [span [@class='content-FujgyDpN'")
            refreshbutton.click()
            print('found refresh button')
        except:
            print("no refresh button found")
        time.sleep(3)
        allnews = get_last_news(html_text, lastnews, allnews)
        for new in lastnews:
            article_txt = read_article(new)
            write_article_to_file(article_txt, 'article.txt')
            call_js_script('article.txt')
        time.sleep(60)

if __name__ == '__main__':
    get_news()

# I'm going to give you a financial news article, you're going to list me all the companies related to this news and tell me for each company, if it should be having a really good, good, neutral, negative, really negative impact on each company. Just write "COMPANY(STOCK SYMBOL): IMPACT". IMPACT can only be "VERY POSITIVE", "POSITIVE", "NEUTRAL", "NEGATIVE", "VERY NEGATIVE" for each enterprise, don't say anything else, you must not say anything else, one entreprise per line, there shouldn't be more than 1 enterprise per line, there shouldn't be line breaks between two lines, you must write "ENTERPRISE(STOCK SYMBOL): IMPACT" for each enterprise. here is the article: