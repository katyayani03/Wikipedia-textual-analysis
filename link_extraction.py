from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

form_link = "https://forms.gle/N14WASGiAhXhD3w7A"
news_site = "https://en.wikipedia.org/wiki/Wikipedia:Good_articles/Engineering_and_technology"

response = requests.get(news_site)
response.raise_for_status()
data = response.text

soup = BeautifulSoup(data, "html.parser")
article_list = soup.select("#mw-content-text > div.mw-content-ltr.mw-parser-output > div.wp-ga-topic > div:nth-child(6) > div.mw-collapsible-content > p > a")
print(len(article_list))
article_links = [("https://en.wikipedia.org/" + i.get("href")) for i in article_list]
article_titles = [i.get("title") for i in article_list]
print(article_links)
print(article_titles)


chrome_options = webdriver.ChromeOptions()  # keeps it open
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)  # create and configure chrome webdriver
driver.get(form_link)
time.sleep(3)
for i in range(len(article_links)):
    title_inp = driver.find_element(By.XPATH,
                                      value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_inp = driver.find_element(By.XPATH,
                                   value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')

    title_inp.send_keys(article_titles[i])
    link_inp.send_keys(article_links[i])
    submit.click()
    submit_another_response = driver.find_element(By.XPATH, value='/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    submit_another_response.click()

driver.quit()
