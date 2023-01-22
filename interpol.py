import re
import time
from datetime import date, datetime, timedelta
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from openpyxl import Workbook
import pandas as pd


Age = []
Place_Of_birth = []
Date_Of_Birth = []
Charges = []
Nationality = []
Fname = []
Forename = []
Images = []
Details = []
Gender = []
Wantedby = []

# Names = list(Fname + Forename)


driver1 = webdriver.Chrome(ChromeDriverManager().install())
driver1.maximize_window()

driver2 = webdriver.Chrome(ChromeDriverManager().install())
driver2.maximize_window()
driver1.get("https://www.interpol.int/en/How-we-work/Notices/View-Red-Notices")
print(driver1.current_url)
driver1.implicitly_wait(10)

for page_num in range(2,10):
    page_check = WebDriverWait(driver1, 180).until(EC.presence_of_element_located((By.XPATH,'//*[@id="noticesResultsItemList"]/div[1]'))).text
    rows = WebDriverWait(driver1, 180).until(EC.presence_of_element_located((By.XPATH, '//*[@id="noticesResults"]/div[2]'))).find_elements(By.CSS_SELECTOR, 'div.redNoticeItem')
    length = len(rows)
    print(length)

    for k in range(0,length):
        html_element =  WebDriverWait(driver1, 180).until(EC.presence_of_element_located((By.XPATH, '//*[@id="noticesResults"]/div[2]'))).find_elements(By.CSS_SELECTOR, 'div.redNoticeItem')[k]

        
        try:
            age = html_element.find_element(By.CSS_SELECTOR,"span.age").text
            Age.append(age)
#             print(age)
        except:
            pass
        
        try:
            nationality = html_element.find_element(By.CSS_SELECTOR,"span.nationalities").text
            Nationality.append(nationality)
#             print(nationality)
        except:
            pass
        
        try:
            detail_page = html_element.find_element(By.CSS_SELECTOR,".redNoticeItem__labelText > a").get_attribute('href')
#             print(detail_page)
        except:
            pass
        
        driver2.get(detail_page)
        driver2.refresh();
        time.sleep(3)
        
        try:    
            fname  = driver2.find_element(By.CSS_SELECTOR,"strong#name").text
            Fname.append(fname)            
#             print(name).split('\n')[0]
        except:
            fname = "NA"
            Fname.append(fname)
            pass
        
        try:
            forename  = driver2.find_element(By.CSS_SELECTOR,"strong#forename").text
            Forename.append(forename)
#             print(forename).split('\n')[1]
        except:
            forename = "NA"
            Forename.append(forename)
            pass
        
        try:
            date_of_birth = driver2.find_element(By.CSS_SELECTOR,"strong#date_of_birth").text
            Date_Of_Birth.append(date_of_birth)
#             print(date_of_birth)
        except:
            pass
        
        try:
            gender = driver2.find_element(By.CSS_SELECTOR,"strong#sex_id").text
            print(gender)
            Gender.append(gender)
#             
        except:
            pass
        
        try:
            wantedby = driver2.find_element(By.XPATH,"//div[2]/div/p/strong").text
            print(wantedby)
            Wantedby.append(wantedby)
#             
        except:
            pass
        
        try:
            place_of_birth = driver2.find_element(By.CSS_SELECTOR,"span#place_of_birth").text
            Place_Of_birth.append(place_of_birth)
#             print(place_of_birth)
        except:
            pass
        
        try:
            charge = driver2.find_element(By.CSS_SELECTOR,"p#charge").text
            Charges.append(charge)
#             print(charge)
        except:
            pass
        
        try:
            image = driver2.find_element(By.CSS_SELECTOR,"div.redNoticeLargePhoto.redNoticeLargePhoto--red > div > img").get_attribute('src')
            Images.append(image)
#             print(image)
        except:
            pass
        
        try:
            details = driver2.find_element(By.XPATH,"//*[@id='singlePanel']/div[2]/div/div[2]/div[4]/table/tbody").text
            print(details)
            Details.append(details)            
        except:
            pass

    try: 
        next_page = WebDriverWait(driver1,30).until(EC.element_to_be_clickable((By.LINK_TEXT,str(page_num))))
        driver1.execute_script("arguments[0].click();",next_page)
        print('Next page')
        WebDriverWait(driver1,20).until_not(EC.text_to_be_present_in_element((By.XPATH,'//*[@id="noticesResultsItemList"]/div[1]'),page_check))

    except:
        print('No Next page')
        
    data_list = {
        "Fname":Fname,
        "Forename ":Forename,
        "Age": Age,
        "Gender": Gender,
        "Place_Of_birth": Place_Of_birth,
        "Date_Of_Birth": Date_Of_Birth,
        "Nationality": Nationality,
        "Details":Details,
        "Images": Images,
        "Wantedby":Wantedby,
    }
    
    df = pd.DataFrame.from_dict(data_list)
    df.transpose()
    df.to_csv("Interpol1.csv",index=False)

    
driver1.quit()
driver2.quit()
