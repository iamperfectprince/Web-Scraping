from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import math
import os
import pandas as pd
import requests
from PIL import Image


 
path = "C:/Users/Public/Interpol"
if not os.path.exists(path):
    os.mkdir(path)

driver1 = webdriver.Chrome(ChromeDriverManager().install())
driver1.get("https://www.interpol.int/en/How-we-work/Notices/View-Red-Notices")
driver1.maximize_window()
print(driver1.current_url)
driver1.implicitly_wait(10)

driver2 = webdriver.Chrome(ChromeDriverManager().install())
driver2.maximize_window()

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



select = Select(driver1.find_element(By.ID,"nationality"))
options = select.options
print("Total nationality is : ",len(options))

        
def search_input(start,end,diff):
    for i in range(start,end,diff):
        start=i+1
        end=i+10
        print(" Current Age Range",start,"-",end)
        
        driver1.find_element(By.ID, 'ageMin').clear()
        driver1.find_element(By.ID,'ageMin').send_keys(start)        
        
        driver1.find_element(By.ID, 'ageMax').clear()
        driver1.find_element(By.ID,'ageMax').send_keys(end)
        
        button = driver1.find_element(By.XPATH,"//*[@id='submit']")
        driver1.execute_script("arguments[0].click();", button)
        time.sleep(5)
        
        try:
            Search_results = int(driver1.find_element(By.ID,"searchResults").text)
            if Search_results > 160:
                new_diff = math.floor(diff/2)
                search_input(start,end,new_diff)
            else:
                try:
                    print("Scaping Started... ")
                    for page_num in range(2,9):
                        page_check = WebDriverWait(driver1, 180).until(EC.presence_of_element_located((By.XPATH,'//*[@id="noticesResultsItemList"]/div[1]'))).text
                        rows = WebDriverWait(driver1, 180).until(EC.presence_of_element_located((By.XPATH, '//*[@id="noticesResults"]/div[2]'))).find_elements(By.CSS_SELECTOR, 'div.redNoticeItem')
                        length = len(rows)
                        print("Total No of Profile on Page=",length)

                        for k in range(0,length):
                            html_element =  WebDriverWait(driver1, 180).until(EC.presence_of_element_located((By.XPATH, '//*[@id="noticesResults"]/div[2]'))).find_elements(By.CSS_SELECTOR, 'div.redNoticeItem')[k]


                            try:
                                age = html_element.find_element(By.CSS_SELECTOR,"span.age").text
                                Age.append(age)
                            except:
                                pass

                            try:
                                nationality = html_element.find_element(By.CSS_SELECTOR,"span.nationalities").text
                                Nationality.append(nationality)
                            except:
                                pass

                            try:
                                detail_page = html_element.find_element(By.CSS_SELECTOR,".redNoticeItem__labelText > a").get_attribute('href')
                            except:
                                pass

                            driver2.get(detail_page)
                            driver2.refresh();
                            time.sleep(3)
                            
                            try:    
                                fname  = driver2.find_element(By.CSS_SELECTOR,"strong#name").text
                                Fname.append(fname)            
                            except:
                                fname = "NA"
                                Fname.append(fname)
                                pass
                            print("NAME: ",fname)

                            try:
                                forename  = driver2.find_element(By.CSS_SELECTOR,"strong#forename").text
                                Forename.append(forename)
                            except:
                                forename = "NA"
                                Forename.append(forename)
                                pass

                            try:
                                date_of_birth = driver2.find_element(By.CSS_SELECTOR,"strong#date_of_birth").text
                                Date_Of_Birth.append(date_of_birth)
                            except:
                                pass

                            try:
                                gender = driver2.find_element(By.CSS_SELECTOR,"strong#sex_id").text
                                print(gender)
                                Gender.append(gender)
                            except:
                                pass

                            try:
                                wantedby = driver2.find_element(By.XPATH,"//div[2]/div/p/strong").text
                                print(wantedby)
                                Wantedby.append(wantedby)
                            except:
                                pass

                            try:
                                place_of_birth = driver2.find_element(By.CSS_SELECTOR,"span#place_of_birth").text
                                Place_Of_birth.append(place_of_birth)
                            except:
                                pass

                            try:
                                charge = driver2.find_element(By.CSS_SELECTOR,"p#charge").text
                                Charges.append(charge)
                                print(charge)
                            except:
                                charge = driver2.find_element(By.XPATH,"//*[@id='charge']").text
                                Charges.append(charge)
                                print(charge)
                                pass

                            try:
                                image = driver2.find_element(By.CSS_SELECTOR,"div.redNoticeLargePhoto.redNoticeLargePhoto--red > div > img").get_attribute('src')
                                Images.append(image)
                                tmp_img_name=fname.replace(" ","_")
                                print(tmp_img_name)
                                img=Image.open(requests.get(image, stream = True).raw)
                                print("link2",image)        
                                img.save('%s/%s.jpg' %(path,tmp_img_name))
                                print("Success Img Downloaded")
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
                            break
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
                        "Charges": Charges,
                    }

                    df = pd.DataFrame.from_dict(data_list)
                    df.transpose()
                    df.to_csv("interpol_stuv.csv",index=False)
                except:
                    pass
            
        except:
            pass

for index in range(1, len(options)):
    country_name=options[index].text
    if re.search('^s|^t|^u|^v.*', country_name, re.IGNORECASE):
        print("Current Country is:-",options[index].text)
        select.select_by_index(index)
        search_input(0,120,10)
    
driver2.quit()
driver1.quit()
