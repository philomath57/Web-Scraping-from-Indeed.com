from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time

driver = webdriver.Chrome('D:/Web Scraping/chromedriver_win32/chromedriver.exe')

driver.get('https:www.google.com')

google_input = driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
google_input.send_keys('indeed')
google_input.send_keys(Keys.ENTER)

indeed_url = driver.find_element(By.XPATH,'//*[@id="rso"]/div[1]/div/div/div/div/div/div/div[1]/a').click()

job_search = driver.find_element(By.XPATH,'//*[@id="text-input-what"]')
job_search.send_keys('Data Analyst')
job_search.send_keys(Keys.ENTER)

df = pd.DataFrame({'Link':[''],'Role':[''],'Company':[''],'Location':[''],'Salary':['']})

i = 0
while i<10:
    soup = BeautifulSoup(driver.page_source,'lxml')

    job_postings = soup.find_all('div',class_='job_seen_beacon')
    
    for jobs in job_postings:
        try:
            link = jobs.find('a',class_='jcs-JobTitle css-jspxzf eu4oa1w0').get('href')
            full_link = 'https://in.indeed.com' + link
        except:
            full_link = 'N/A'
        try:
            
            Role = jobs.find('h2',class_='jobTitle css-1h4a4n5 eu4oa1w0').text
        except:
            Role = 'N/A'
        try:
            company = jobs.find('span',class_='companyName').text
        except:
             company = 'N/A'
        try:
            location = jobs.find('div',class_='companyLocation').text
        except:
             location = 'N/A'
        try:
            salary = jobs.find('div',class_='attribute_snippet').text
        except:
             salary = 'N/A'
             df = df.append({'Link':full_link,'Role':Role,'Company':company,'Location':location,'Salary':salary},ignore_index=True)
    try:
        next_page = soup.find('a',class_='css-cy0uue e8ju0x50').get('href')
        driver.get('https://in.indeed.com' + next_page)
    except:
        break
    i = i + 1
    
df.to_csv('D:/Web Scraping/Indeed_job.csv')

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders


sender = 'mdfaiyazalam17091995@gmail.com'
receiver = 'mdfaiyazalam17091995@gmail.com'

msg = MIMEMultipart()
msg['Subject'] = 'Jobs on Indeed'
msg['From'] = sender
msg['To'] = receiver


part = MIMEBase('application','octet-stream')
part.set_payload(open('D:/Web Scraping/Indeed_Job.csv','rb').read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachement; filename="Indeed_Job.csv"')

s = smtplib.SMTP_SSL(host='smtp.gmail.com',port=534)
s.login(user='mdfaiyazalam17091995@gmail.com',password='Iambrock57')
s.sendmail(sender,receiver,msg.as_string())
s.quit()








    


