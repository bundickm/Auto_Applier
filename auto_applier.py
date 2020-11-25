import os
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from personal_info import INFO


# Testing only
LEVER_SAMPLE = 'https://jobs.lever.co/matchgroup/b2e5a860-e36a-4519-916e-26debd95060b/apply?lever-source=Glassdoor'
URLS = [LEVER_SAMPLE]


def lever_apply(driver):
    '''Apply to jobs that use Lever'''
    try:
        driver.find_element_by_class_name('template-btn-submit').click()
        time.sleep(15)
    except:
        pass

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
    except:
        pass

    # Social Media
    driver.find_element_by_name('urls[LinkedIn]').send_keys(INFO['linkedin'])
    driver.find_element_by_name('urls[Twitter]').send_keys(INFO['twitter'])
    driver.find_element_by_name('urls[Portfolio]').send_keys(INFO['website'])
    try:
        driver.find_element_by_name('urls[GitHub]').send_keys(INFO['github'])
    except:
        try:
            driver.find_element_by_name('urls[Github]').send_keys(INFO['github'])
        except:
            pass

    # Diversity Questions
    # May need rework but not necessary due to it being unrequired fields
    # try:
    #     driver.find_element_by_xpath('//*[@id="countrySurvey "]/ul/li[1]/div[2]/ul/li[1]/label/span').click()
    #     driver.find_element_by_xpath('//*[@id="countrySurvey "]/ul/li[2]/div[2]/ul/li[2]/label/span').click()
    #     driver.find_element_by_xpath('//*[@id="countrySurvey "]/ul/li[3]/div[2]/ul/li[3]/label/span').click()
    # except:
    #     pass
    
    # How you found out
    try:
        driver.find_element_by_class_name('application-dropdown').click()
        search = driver.find_element_by_xpath("//select/option[text()='Glassdoor']").click()
    except:
        pass

    # Upload Resume and Hit Submit
    driver.find_element_by_name('resume').send_keys(os.getcwd()+ '/' + INFO['resume'])
    time.sleep(30)
    # driver.find_element_by_class_name('template-btn-submit').click()

if __name__ == '__main__':
    jobs_applied_to = pd.read_csv('jobs_applied_to.csv')
    unapplied_for = pd.read_csv('unapplied_for.csv')
    driver = webdriver.Chrome(executable_path=(os.getcwd() + '/chromedriver'))
    df = pd.read_csv(os.getcwd() + '/Data_Scientist_jobs.csv')
    job_links = df['0'].to_list()

    for url in job_links:
        if url in jobs_applied_to['job_links']:
            continue
        if 'lever' in url:
            driver.get(url)
            try:
                lever_apply(driver)
                jobs_applied_to = jobs_applied_to.append({'job_links': url}, ignore_index=True)
                jobs_applied_to.to_csv('jobs_applied_to.csv', index=False)
            except:
                continue
        else:
            unapplied_for = unapplied_for.append({'job_links': url}, ignore_index=True)
    unapplied_for.to_csv('unapplied_for.csv', index=False)
    time.sleep(5)

    driver.close()