import os
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


# Testing only
LEVER_SAMPLE = 'https://jobs.lever.co/matchgroup/e58fb8a9-60e9-48a9-bd60-e791472b1312?lever-source=Indeed'
URLS = [LEVER_SAMPLE]

### Need to move this to a separate file and add it to git ignore ###
INFO = {
    'first_name': 'John',
    'last_name': 'Doe',
    'email': 'fake@fakerson.com',
    'phone': '555-555-5555',
    'current_company': 'Hydra',
    'resume': 'fake_resume.pdf',
    'resume_textfile': 'fake_resume_short.txt',
    'linkedin': 'https://www.linkedin.com/',
    'website': 'google.com',
    'github': 'https://github.com',
    'twitter': 'www.twitter.com',
    'location': 'Los Angeles, California, United States',
    'grad_month': '12',
    'grad_year': '2008',
    'university': 'Hogwarts'}
INFO['full_name'] = INFO['first_name'] + ' ' + INFO['last_name'],


def lever_apply(driver):
    '''Apply to jobs that use Lever'''
    driver.find_element_by_class_name('template-btn-submit').click()
    time.sleep(15)
    
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
    '''Still Need'''
    
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
            except Exception:
                continue

        time.sleep(5)

    driver.close()
