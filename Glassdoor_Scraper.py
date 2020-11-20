import os
import re
import time
import pandas as pd
from urllib import request
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException, NoSuchElementException


POSITIONS = ['Data Scientist']
CHROME_DRIVER_PATH = os.getcwd() + '/chromedriver'
PAGE_LOAD = 30
MAX_PAGES = 2


def login(driver):
    '''Load Glassdoor and then wait for login'''
    driver.get('https://www.glassdoor.com/index.htm')

    while True:
        try:
            WebDriverWait(driver, 1).until(expected_conditions.url_contains("member"))
        except TimeoutException:
            break
    return True


def search_for_position(driver):
    time.sleep(PAGE_LOAD)

    try:
        position_to_search_for = driver.find_element_by_xpath("//*[@id='sc.keyword']")
        position_to_search_for.send_keys(POSITIONS[0])
        driver.find_element_by_xpath(" //*[@id='scBar']/div/button").click()

        return True
    except NoSuchElementException:
        return False


def clean_links(filtered_links):
    cleaned_links = []

    for link in filtered_links:
        # Correct the address
        link = link.replace("GD_JOB_AD", "GD_JOB_VIEW")
        if link[0] == '/':
            link = f"https://www.glassdoor.com{link}"

        # Open the link and get the redirected URL
        a_request = request.Request(link, None, {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0'})
        try:
            response = request.urlopen(a_request)
            redirect = response.geturl()

            # Skip Easy Applies
            if "glassdoor" not in redirect:
                cleaned_links.append(redirect)
        except Exception:
            pass
    
    return set(cleaned_links)


def get_links(driver):
    '''Get all the job links, excluding easy apply and errors'''
    time.sleep(PAGE_LOAD)

    # Use BS to sift throught the HTML
    page_source = driver.page_source
    soup = BS(page_source, features='lxml')
    job_links = soup.findAll("a", {"class": "jobLink"})
    filtered_links = [job_link['href'] for job_link in job_links]

    return filtered_links


def scrape_job_links():
    '''Scrape and compile all job links'''
    page = 1
    all_links = set()
    next_url = ''
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)

    if not (login(driver) and search_for_position(driver)):
        driver.close()

    while page < MAX_PAGES:
        print('Page Num:', page)
        if page == 1:
            all_links.update(clean_links(get_links(driver)))

            # Next page then update page and url
            next_page = driver.find_element_by_xpath("//*[@id='FooterPageNav']/div/ul/li[3]/a")
            this_page = next_page.get_attribute('href')
            page_num = re.search('(?P<url>[^;]*?)(?P<page>.htm\?p=)(?P<pagenum>.)', this_page)
            page += 1
            next_url = f"{page_num.group('url')}_IP{page}.htm"

        if page >=2 :
            driver.get(next_url)
            all_links.update(clean_links(get_links(driver)))

            # Next page then update page and url
            page_num = re.search('(?P<url>[^;]*?)(?P<pagenum>.)(?P<html>.htm)', next_url)
            page += 1
            next_url = f"{page_num.group('url')}{page}.htm"

    driver.close()
    return all_links

def links_to_csv():
    csv_name = (POSITIONS[0] + '_jobs.csv').replace(' ', '_')
    job_links = scrape_job_links()
    print(job_links)

    df = pd.DataFrame(job_links)
    df.to_csv(csv_name)

links_to_csv()
