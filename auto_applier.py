import os
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from personal_info import INFO


# Testing only
LEVER_SAMPLE = 'https://jobs.lever.co/matchgroup/e58fb8a9-60e9-48a9-bd60-e791472b1312?lever-source=Indeed'
URLS = [LEVER_SAMPLE]


def lever_apply(driver):
    '''Apply to jobs that use Lever'''
    driver.find_element_by_class_name('template-btn-submit').click()
    time.sleep(15)
    driver.find_element_by_xpath('/html/body/div[1]/div/a').click()

    # Basics
    driver.find_element_by_name('name').send_keys(INFO['full_name'])
    driver.find_element_by_name('email').send_keys(INFO['email'])
    driver.find_element_by_name('phone').send_keys(INFO['phone'])
    driver.find_element_by_name('org').send_keys(INFO['current_company'])

    # Education
    try:
        driver.find_element_by_class_name('application-university').click()
        search = driver.find_element_by_xpath("//*[@type='search']")
        search.send_keys(INFO['university'])
        search.send_keys(Keys.RETURN)
    except NoSuchElementException:
        pass

    # Social Media
    driver.find_element_by_name('urls[LinkedIn]').send_keys(INFO['linkedin'])
    driver.find_element_by_name('urls[Twitter]').send_keys(INFO['twitter'])
    try:
        driver.find_element_by_name('urls[Github]').send_keys(INFO['github'])
    except NoSuchElementException:
        pass
    driver.find_element_by_name('urls[Portfolio]').send_keys(INFO['website'])

    # Diversity Questions
    try:
        driver.find_element_by_xpath('//*[@id="countrySurvey "]/ul/li[1]/div[2]/ul/li[1]/label/span').click()
        driver.find_element_by_xpath('//*[@id="countrySurvey "]/ul/li[2]/div[2]/ul/li[2]/label/span').click()
        driver.find_element_by_xpath('//*[@id="countrySurvey "]/ul/li[3]/div[2]/ul/li[3]/label/span').click()
    except:
        pass
    
    # How you found out
    try:
        driver.find_element_by_class_name('application-dropdown').click()
        search = driver.find_element_by_xpath("//select/option[text()='Glassdoor']").click()
    except NoSuchElementException:
        pass

    # Upload Resume and Hit Submit
    driver.find_element_by_name('resume').send_keys(os.getcwd()+ '/' + INFO['resume'])
    # driver.find_element_by_class_name('template-btn-submit').click()

if __name__ == '__main__':
    driver = webdriver.Chrome(executable_path=(os.getcwd() + '/chromedriver'))
    # df = pd.read_csv(os.getcwd() + '/Data_Scientist_jobs.csv')
    # job_links = df['0'].to_list()

    for url in URLS:
        if 'lever' in url:
            driver.get(url)
            try:
                lever_apply(driver)
                time.sleep(60)
            except Exception:
                continue

        time.sleep(5)

    driver.close()
