import csv
import ftplib
import json
import os
import random
import time
from datetime import datetime
from pathlib import Path

import psutil
import pyautogui

from functions_file import *
from word_sorter import df_dups_removed

cwd_path = Path.cwd()

used_verbs = Path(f'{cwd_path}/used-words-lists/used_verbs.csv')

start_time = datetime.now()

# #### NON-REUSABLE FUNCTIONS ####

def rand_verb_generator(d_frame):
    
    """Takes in a DataFrame and generates a random verb

    Returns:
        df (DataFrame) - Pandas Dataframe of verbs.csv.
        rand_verb (String) - a randomly picked verb.
        rand_ing_verb (String) - the "present participle" of the randomly picked verb eg. ends in "ing".
        
    """

    df_func = d_frame.copy(deep=True) # ORIG Length of df 9642 without duplicates
    
    rand_num = random.randrange(0, len(df_func))

    rand_verb = df_func['verb'][rand_num]

    rand_ing_verb = df_func['present participle (ing)'][rand_num]
    
    return df_func, rand_verb, rand_ing_verb

#### FIND PID NUMBER OF GIMP PROCESS TO BE ABLE TO CHECK IF IT IS RUNNING OR NOT LATER ####

def find_process_id_by_name(process_name):

    """Get a list of PIDs with the given string process_name

    Returns:
        list: list of Process IDs using process_name
    """

    list_of_process_objects = []
    #Iterate over the all the running process
    for proc in psutil.process_iter():
       try:
           pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
           # Check if process name contains the given name string.
           if process_name.lower() in pinfo['name'].lower() :
               list_of_process_objects.append(pinfo)
       except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
           pass
    return list_of_process_objects

gimp_pid = ''

#### CHECKS IF GIMP IS OPEN AND, IF NOT, OPENS IT ####

def gimp_running_chk():
    
    """Checks if process is running (GIMP) and opens it if it's not

    Returns:
        gimp_pid (integer): Process ID of process_name in find_process_id_by_name(process_name).
        
    """

    while True:
        
        gimp_process = find_process_id_by_name('gimp-2.10')
        
        if gimp_process == []:
            print("Gimp not open.")
            os.startfile('C:\\Program Files\\GIMP 2\\bin\\gimp-2.10.exe')
            time.sleep(3)
            continue
        
        elif gimp_process[0]['name'] == 'gimp-2.10.exe':
            print("Gimp is open/ing.")
            gimp_pid = gimp_process[0]['pid']
            break
    
    return gimp_pid

def list_to_string(res): 
    
    """Takes in a List and spews out a String

    Returns:
        String: Returns a String from a List
    """
    
    str1 = " or " 
    
    # return string  
    return (str1.join(res))

############################################# END OF DEFS ######################################################

gimp_pid = gimp_running_chk()

verified_verbs = []
used_verb_counter = []
while len(verified_verbs) < 1:  # number of designs to generate
    
    while True:
        rand_ing_verb = rand_verb_generator(df_dups_removed)
        rand_ing_verb = rand_ing_verb[2]
        
        sesame = opening_docs()

        verbs_reader = sesame[0]
        just_syns_verb_writer = sesame[1]
        
        thesaurus_entry = access_thesaurus_api(rand_ing_verb)
        aktch_thes_dict = thesaurus_entry[3]
        
        for verbage in verbs_reader:
            if verbage[4] == rand_ing_verb:
                with open(used_verbs, 'a', newline='') as used_vbs:
                    writer = csv.writer(used_vbs)
                    writer.writerow(verbage)
                    used_verb_counter.append(verbage[4])
                    
                    
        if isinstance(aktch_thes_dict, str) == True:
            for vbs in verbs_reader:
                if vbs[4] == rand_ing_verb:
                    just_syns_verb_writer.writerow(vbs)
            continue
        
        elif isinstance(aktch_thes_dict, dict) == True:
            pass

        verify = input(f"Is {rand_ing_verb} OK? ").upper()
        
        if verify == "Y":
            
            verified_verbs.append(rand_ing_verb)
            
            break

### ONCE HERE WE HAVE A LIST OF VERIFIED VERBS ####

with open('verbs_to_gimp.txt', mode='w', ) as verbs_to_gimp:    # write verified verbs to verb_to_gimp.txt
    for item in verified_verbs:                                 # this is needed to bridge the gimp gap
        verbs_to_gimp.write(f'{item}\n')

for ver in verified_verbs:
    
    specific_verb = verb_types(ver)
    spec_verb = specific_verb[0]
    spec_past = specific_verb[2]
    spec_ing_verb = specific_verb[4]

    thesaurus_entry = access_thesaurus_api(spec_verb)
    thes_dict = thesaurus_entry[2]

    json_number = len(thes_dict)    

    def_short_list = syns_and_descripsh(thes_dict, json_number)[0][:3]

    res = [', '.join(ele) for ele in def_short_list]

    definition = list_to_string(res)
    
    synonyms = syns_and_descripsh(thes_dict, json_number)[1]
    syns_sorted = syns_and_descripsh(thes_dict, json_number)[1][:5] # restricts synonyms list to 5 items and ready to be sorted
    syns_sorted.sort()
    syns_reversed = syns_and_descripsh(thes_dict, json_number)[1][:9] # restricts synonyms list to 5 items and ready to be sorted
    syns_reversed.sort(reverse=True)    
    
    specific_verb = verb_types(ver)
    spec_verb = specific_verb[0]
    spec_past = specific_verb[2]
    spec_ing_verb = specific_verb[4]
    
    str_synonyms_3 = ", ".join(synonyms[0:3])
    str_synonyms_5 = ", ".join(syns_sorted)    
    str_synonyms_9 = ", ".join(syns_reversed)

#### TITLES AND DESCRIPTIONS ####

    pre_title = f"Get {spec_ing_verb.capitalize()}! Funny Gorilla and Cat Design\n\n" # 60 characters
    title = pre_title[:60] # the 'pre' variables might be too long for the fields so need to be sliced just in case

    brand = "JVZ Designs\n\n" # 50 characters

    pre_feature1 = f"Unique '{spec_ing_verb}' slogan design for you or the {str_synonyms_3} related loving person in your life.\n\n" # 256 characters
    feature1 = pre_feature1[:256]

    pre_feature2 = f"Funny design for the lovers of {str_synonyms_5} and {spec_past} stuff! No apes were hurt by cats or kittens during the making of this design.\n\n" # 256 characters
    feature2 = pre_feature2[:256]
    
    pre_description = f"This original design was very much inspired by similar verb-age along the lines of {str_synonyms_9} ie. {spec_ing_verb}-related verb-age. It should appeal to those who really understand things like '{definition}'. JVZ Designs provides original, geek, nerd, funny, fantasy, sci fi, cartoon, comic, and sometimes {spec_verb}-centric designs for the type of cool and awesome people who want to make the world a better place by having one of my images on their stuff." # min 75 chars max 2000 characters
    description = pre_description[:2000]
    
#### MAKING FILES FOR THE BLURBS FOLDER ####
    
    blurb_file_name = Path(f'{cwd_path}/blurbs/get_{spec_ing_verb}.txt')

    with open(blurb_file_name, mode="w") as blurb_text:
        
        blurb_text.write(title)
        blurb_text.write(brand)
        blurb_text.write(feature1)
        blurb_text.write(feature2)
        blurb_text.write(description)
        
### THE FRANKLY AWESOME GIMP AUTO DESIGNER INSTIGATOR ***AND*** PROCESS MEASURER TO LEAD INTO UPLOADING TO AMAZON ####

pyautogui.moveTo(561, 749) # moves to gimp icon on task bar
pyautogui.click()
time.sleep(1)
pyautogui.hotkey('ctrl', 'shift', 'k')
time.sleep(1)
pyautogui.moveTo(600, 749) # moves to gimp icon on task bar
pyautogui.click()

chk_cpu = []

gimp_process = psutil.Process(gimp_pid) # gimp_pid specified above from find_process_id_by_name()

for x in range(0, 40):
    x = gimp_process.cpu_percent(interval=8)
    print("Waiting for this to be 0.0: ", x)
    if x == 0.0:
        break
    else:
        continue

print("OUT OF LOOP AND CARRYING ON...")

#### ALL FILES AND FOLDERS SHOULD BE SET UP, SOOOOO ONTO TO AMAZON... ####
    
#### THIS OPENS AND RUNS amazon_uploader.py ####

amazon_uploader = Path(f'{cwd_path}/amazon_uploader.py')
exec(open(amazon_uploader).read())

#### THIS OPENS AND RUNS web_page_maker.py ####

web_page_maker = Path(f'{cwd_path}/web_page_maker.py')
exec(open(web_page_maker).read())

#### UPLOAD ALL FILES IN blurbs AND images

pwords = open('login_json_WARNING.json') # named to remind me not to upload the JSON file
data = json.loads(pwords.read())

ftp_user = data['ftp_user']
ftp_pass = data['ftp_pass']

for blurb_file in os.listdir(Path(f'{cwd_path}/blurbs')):
    outputfile = Path(f'{cwd_path}/blurbs/{blurb_file}')

    ftp = ftplib.FTP('ftp.jvzdesigns.com', ftp_user, ftp_pass)
    file = open(outputfile, 'rb') # file to send
    ftp.cwd('get-stuff/UPLOADED/uploaded_blurbs/') # needs the trailing forward slash
    ftp.storbinary(f'STOR {blurb_file}', file)     # send the file
    file.close()                                    # close file and FTP

ftp.quit()

#### MOVING FILES AND FOLDERS OUT OF blurbs AND images AND INTO 'UPLOADED'. ####

blurbs = Path(f'{cwd_path}/blurbs')
uploaded_blurbs = Path(f'{cwd_path}/UPLOADED/uploaded_blurbs')

move_files(blurbs, uploaded_blurbs)

images = Path(f'{cwd_path}/images')
uploaded_images = Path(f'{cwd_path}/UPLOADED/uploaded_images')

move_files(images, uploaded_images)

# EXECUTION TIMER 

end_time = datetime.now()

duration = end_time - start_time
duration = str(duration).split(".")[0]
print(f'Duration: {duration}')

#### WRITE REPORT TO report.csv OF Date, No. Uploaded on Date, Duration, Tot. Uploaded

report_list = []

today = datetime.now()

date_now = today.strftime("%d/%m/%Y : %H:%M")

url = "http://www.jvzdesigns.com/get-stuff/get-thumbs/"

online_files = find_online_files(url)
len_uploaded_thumbs_list = online_files[1]

report_list.append(date_now) # Today's date and time
report_list.append(len(verified_verbs)) # Number of files uploaded in that run of the script
report_list.append(f'{duration}') # How long the script took to run
report_list.append(len_uploaded_thumbs_list) # Number of designs uploaded overall
report_list.append(len(df_dups_removed.index) - len(used_verb_counter)) # Numer of Verbs left in the list
report_list.append(len(used_verb_counter)) # Number of verbs that should have been added to used_verbs.csv
report_list = [report_list]
print("Report details sent to design-o-matic-report.csv: ", report_list)

report_path = Path(f'{cwd_path}/used-words-lists/design-o-matic-report.csv')
with open(report_path, mode='a') as r_file:
    report_csv = csv.writer(r_file)
    report_csv.writerows(report_list)
    
# UPLOAD THE NOW UPDATED used_verbs.csv AND just_syns.csv TO BE USED TO PULL DATA FROM NEXT TIME WE RUN THE SCRIPT

f = open('login_json_WARNING.json') # named to remind me not to upload the JSON file
data = json.loads(f.read())

ftp_user = data['ftp_user']
ftp_pass = data['ftp_pass']

for csv_file in os.listdir(Path(f'{cwd_path}/used-words-lists')):
    outputfile = Path(f'{cwd_path}/used-words-lists/{csv_file}')

    ftp = ftplib.FTP('ftp.jvzdesigns.com', ftp_user, ftp_pass)
    file = open(outputfile, 'rb') # file to send
    ftp.cwd('get-stuff/word-lists-etc/') # needs the trailing forward slash
    ftp.storbinary(f'STOR {csv_file}', file)     # send the file
    file.close()                                    # close file and FTP

ftp.quit()
print("Verbs used in this run: ", verified_verbs)
print("Done!!!")

#### END ? ####
