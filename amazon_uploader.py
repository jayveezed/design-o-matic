import json
import os
import time
import pyautogui
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

cwd_path = Path.cwd()

chrome_exe = 'C:\Program Files\Google\Chrome\Application\chromedriver.exe' # check your hea... directory

f = open('login_json_WARNING.json') # named to remind me not to upload the JSON file
data = json.loads(f.read())

username = data['username']
password = data['password']

driver = webdriver.Chrome(chrome_exe)

driver.get('https://merch.amazon.com/designs/new') # .get() allegedly waits for the page to load

driver.maximize_window()

try:

    driver.find_element(By.ID, "ap_email").send_keys(username)

    driver.find_element(By.ID, "ap_password").send_keys(password)

    driver.find_element(By.ID, "signInSubmit").click()

except:
    
    time.sleep(150) # give time to deal with extra security

# LOOP FROM HERE 
blurbs_path = Path(f'{cwd_path}/blurbs')
blurb_files_list = os.listdir(blurbs_path)

for file_num in range(0, len(blurb_files_list)):

    blurb_file = blurb_files_list[file_num]
    lines = []
    blurbs = Path(f'{cwd_path}/blurbs/{blurb_file}')
    with open(blurbs, "r") as blurb_text:

        for line in blurb_text:
            line = line.strip('\n\r')
            lines.append(line)

            lines = [x for x in lines if x]
    
    design_title = lines[0]
    brand_name_text = lines[1]
    bullet_one = lines[2]
    bullet_two = lines[3]
    descripsh = lines[4]     

    img_dir = Path(f'{cwd_path}/images')
    
    img_files = os.listdir(img_dir) # this is where the images are located

    img_folder = Path(f"{cwd_path}/images/{img_files[file_num]}") # path to img_files
    print("Image folder PATH: ", img_folder)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="global-uploader-container"]/div')))

    driver.find_element(By.XPATH, '//*[@id="global-uploader-container"]/div').click()

    # GIVE DIAG BOX TIME TO POP UP

    time.sleep(2)

    pyautogui.write(f'{img_folder}') 
    pyautogui.press('enter')

    time.sleep(15)

    driver.find_element(By.ID, 'designCreator-productEditor-title').send_keys(design_title)
    
   

    driver.find_element(By.ID, 'designCreator-productEditor-brandName').send_keys(brand_name_text)

   

    driver.find_element(By.ID, 'designCreator-productEditor-featureBullet1').send_keys(bullet_one)


    driver.find_element(By.ID, 'designCreator-productEditor-featureBullet2').send_keys(bullet_two)


    driver.find_element(By.ID, 'designCreator-productEditor-description').send_keys(descripsh)

    time.sleep(2)
    
    # driver.find_element(By.ID, 'draft-button').click() # save as draft
    
    driver.find_element(By.XPATH, '/html/body/div[1]/div/app-root/div/div[2]/ng-component/div/product-config-editor/div[5]/button[3]').click()
    
    time.sleep(2)
    
    driver.find_element(By.XPATH, '/html/body/ngb-modal-window/div/div/ng-component/div[2]/div[2]/button[2]').click() # confirmation of submit
    
    time.sleep(5)
    
    driver.find_element(By.ID, 'redirect-designs-new').click() # after confirmation of sub go to create.
    
driver.quit() # close window