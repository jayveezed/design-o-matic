import csv
import json
import os
import shutil
from pathlib import Path

import requests
from bs4 import BeautifulSoup

cwd_path = Path.cwd()
just_syns_path = Path(f'{cwd_path}/used-words-lists/just_syns_verbs.csv')
used_verbs_path = Path(f'{cwd_path}/used-words-lists/used_verbs.csv')
#### CALLS MIRIAM WEBSTER THESAURUS API

def access_thesaurus_api(rand_verb):
    
    """Takes in a word and returns response/result from the MIRIAM WEBSTER THESAURUS API

    Returns:
        thes_response(json) : requests full descriptions and synonyms for the relevant word ie. rand_verb.
        new_dict - the json response of the word used.
        thes_str - the json.dumps response of the word used.
        thes_dict - the json.loads response of the word used.
        aktch_thes_dict - the python dictionary used to extract synonyms and definitions.
        
    """
    f = open('login_json_WARNING.json') # named to remind me not to upload the JSON file
    data = json.loads(f.read())

    api_key = data['thesaurus_api_key']
    
    thes_response = requests.get(f"https://www.dictionaryapi.com/api/v3/references/thesaurus/json/{rand_verb}?key={api_key}")
    
    new_dict = thes_response.json()

    thes_str = json.dumps(new_dict)
    thes_dict = json.loads(thes_str)
    aktch_thes_dict = thes_dict[0]
    
    return new_dict, thes_str, thes_dict, aktch_thes_dict, thes_response

############# OPEN DOCS TO BE READ/WRITTEN TO FUNCTION  ######
        
def opening_docs():
    
    """Opens specified docs for writing, appending, reading:

    Returns:
        verbs_reader - Reads original verbs.csv file.
        just_syns_verb_writer - writes API responses with no definitions to 'just_syns_verbs.csv'.
        used_verbs_reader - verbs that have been uploaded and gone through vetting.
   
    """
    
    orig_verbs_csv = open("verbs.csv", mode="r")
    just_syns_verbs = open(just_syns_path, mode='a', newline='')
    all_used_verbs_csv = open(used_verbs_path, mode="r")

    verbs_reader = csv.reader(orig_verbs_csv)
    just_syns_verb_writer = csv.writer(just_syns_verbs)
    used_verbs_reader = csv.reader(all_used_verbs_csv)

    return verbs_reader, just_syns_verb_writer, used_verbs_reader

def verb_types(current_ing_verb):
    
    """Takes in a string of a verb ending "ing"

    Returns:
        Reads the verb and returns one of the following variants:
        
        vb[0] = verb, 
        vb[1] = present tense, 
        vb[2] = past tense, 
        vb[3] = past participle, 
        vb[4] = present participle (ing).
        
    """
    
    with open("verbs.csv", mode="r") as orig_verbs_csv:

        verbs_reader = csv.reader(orig_verbs_csv)
        for vb in verbs_reader:
            if vb[4] == current_ing_verb:
                return vb[0], vb[1], vb[2], vb[3], vb[4]

# specific_verb = verb_types("blowing")
# spec_verb = specific_verb[0]
# spec_present = specific_verb[1]
# spec_past = specific_verb[2]
# spec_past_partic = specific_verb[3]
# spec_ing_verb = specific_verb[4]

thesaurus_entry = access_thesaurus_api("step")
thes_dict = thesaurus_entry[2]
json_number = len(thes_dict)


# print("Thesaurus entry: ", thesaurus_entry)
# print("thes_dict: ", thes_dict)
# print("json_number: ", json_number)


def syns_and_descripsh(thes_dict, json_number):
    
    """Takes in 'thes_dict' from 'access_thesaurus_api' function and 
    'json_number' ie. len(thes_dict)
   
   Returns:
        synonyms - a list of all synonyms for word used to create 'thes_dict'.
   
        definition_list - a list of lists of definitions of the orignal word
        looked up to create 'thes_dict'.
        
    """
    
    synonyms = []
    definition_list = []
    
    for entry in range(0, json_number):
        
        if thes_dict[entry]['fl'] == 'verb':
            definition_list.append(thes_dict[entry]['shortdef'])
            
            for syn in thes_dict[entry]['meta']['syns']:
                for each in [syn][0][:3]:
                    synonyms.append(each)
        else:
            pass
    
    return definition_list, synonyms


# FUNCTION TO MOVE BLURBS AND IMAGES TO UPLOADED FOLDER

def move_files(source, dest):
    
    ''' Takes in source folder and moves it's files to destination folder '''
    
    source_list = os.listdir(source)

    for i in source_list:
        src_path = Path(f'{source}/{i}')
        shutil.move(src_path, dest)

def find_online_files(url):
    
    """List files in an online directory

    Returns:
        list: List of files in directory "url". Is indexed to start from 5 because
        hidden files and chosen directory are the first 5 entries in the list
        
        int: length of the list
        
        list: of list of just "ing" verbs without "get_" or the file ext.
    """
    response = requests.get(url)
    response_text = response.text
    soup = BeautifulSoup(response_text, 'html.parser')

    hrefs = []

    for a in soup.find_all('a'):
        hrefs.append(a['href'])
        
    uploaded_thumbs_list = hrefs[5:]
    verb_ing_list = []
    
    for b in uploaded_thumbs_list:
        verb_ing_list.append(b[4:-4])
    
    len_uploaded_thumbs_list = len(uploaded_thumbs_list)
    
    return uploaded_thumbs_list, len_uploaded_thumbs_list, verb_ing_list


