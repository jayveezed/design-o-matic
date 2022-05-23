import ftplib
import json
import os
from pathlib import Path
from webbrowser import get

import jinja2
import tinify
from PIL import Image

from functions_file import find_online_files
from amazon_links_diksh import amazon_links_diksh


def divided_cols(orig_list):
    
    """Takes in list of imgs to work out how many imgs per column on web page

    Returns:
        column (integer): number of images divided by 3.
        column_mod (integer): modulus of the calculation.
        column1 - 3 (integer): number of images in the column.

    """
    
    column = int(len(orig_list) / 3)
    column_mod = int(len(orig_list) % 3)

    column1 = orig_list[0:column]
    column2 = orig_list[column:column*2]
    column3 = orig_list[column*2:column*3]
    
    return column, column_mod, column1, column2, column3

####

cwd_path = Path.cwd()

web_dir = Path('C:/wamp64/www/get-stuff')
mob_web_dir = Path('C:/wamp64/www/mobile')

#### GRAB TINIFY KEY FROM JSON FILE

f = open('login_json_WARNING.json') # named to remind me not to upload the JSON file
data = json.loads(f.read())

tinify_key = data['tinify_key']

tinify.key = tinify_key

source = Path(f"{cwd_path}/images")
web_imgs_source = Path(f"{cwd_path}/web_pages/images")

list_of_imgs = os.listdir(source)

for file_name in list_of_imgs:
    
    img_file = Path(f'{source}/{file_name}')
    
    image = Image.open(img_file) # opens image file
    image.thumbnail((450, 540), Image.Resampling.LANCZOS) # changes image size
    image.save(Path(f'{web_imgs_source}/cropped.png'))

    image = Image.open(Path(f'{web_imgs_source}/background-01.png'))
    logo = Image.open(Path(f'{web_imgs_source}/cropped.png'))
    image_copy = image.copy()
    position = ((77, 14))
    image_copy.paste(logo, position, logo)
    image_copy.save(Path(f'{web_imgs_source}/black_bg.png'))

    image = Image.open(Path(f'{web_imgs_source}/black_bg.png'))
    logo = Image.open(Path(f'{web_imgs_source}/background-02.png'))
    image_copy = image.copy()
    position = ((0,0))
    image_copy.paste(logo, position, logo)
    image_copy.save(Path(f'{web_imgs_source}/resized-600x400/{file_name}'))
    
#### HERE WE HAVE UNCOMPRESSED IMGS 600x400 IN resized-600x400 ####
    
### TINYFY ####

for resized in list_of_imgs:
    
    if resized in os.listdir(Path(f'{web_imgs_source}/resized-600x400/')):
        
        source = tinify.from_file(Path(f'{web_imgs_source}/resized-600x400/{resized}'))
        source.to_file(Path(f"{web_imgs_source}/optimised-600x400/{resized[:-4]}.jpg"))

#### HERE WE HAVE OPTIMISED, 600px x 400px VERSIONS OF THE IMG/S IN optimised-600x400

#### RESIZE OPTIMISED IMAGE/S TO THUMBNAIL SIZE (300px x 200px) ####

for orig_file_name in list_of_imgs:
    
    if f'{orig_file_name[:-4]}.jpg' in os.listdir(Path(f'{web_imgs_source}/optimised-600x400/')):
    
        img_file = Path(f'{web_imgs_source}/optimised-600x400/{orig_file_name[:-4]}.jpg')
        image = Image.open(img_file).convert('RGB') # opens image file
        image.thumbnail((300, 200), Image.Resampling.LANCZOS) # changes image size
        image.save(Path(f'{web_imgs_source}/optimised-thumbs/{orig_file_name[:-4]}.jpg'))

#### ALL IMAGES NOW READY TO BE UPLOADED


opt_upload_folder = f'{web_imgs_source}/optimised-thumbs/'

f = open(Path(f'{cwd_path}/login_json_WARNING.json')) # named to remind me not to upload the JSON file
data = json.loads(f.read())

ftp_user = data['ftp_user']
ftp_pass = data['ftp_pass']

for opt in list_of_imgs:
    
    uploadable = f'{opt[:-4]}.jpg'
    
    if f'{opt[:-4]}.jpg' in os.listdir(opt_upload_folder):
    
        ftp = ftplib.FTP('ftp.jvzdesigns.com', ftp_user, ftp_pass)
        file = open(f'{opt_upload_folder}{opt[:-4]}.jpg', 'rb') # file to send
        ftp.cwd('get-stuff/get-thumbs/')
        ftp.storbinary(f'STOR {uploadable}', file)     # send the file
        file.close()                                    # close file and FTP
        
        print("Uploading thumbnails...")

### CREATE get-stuff.php PAGE USING ALL IMAGES UPLOADED TO AMAZON

url = "http://www.jvzdesigns.com/get-stuff/get-thumbs/"

files_list = find_online_files(url)

uploaded_thumbs_list = files_list[0]

divided = divided_cols(uploaded_thumbs_list)

column = divided[0]
column_mod = divided[1]

if column_mod == 1:
    column1 = divided[2]
    column2 = divided[3]
    column3 = divided[4]
    column1.append(uploaded_thumbs_list[-1]) # adds the left over img to column 1
    
elif column_mod == 2:
    column1 = divided[2]
    column2 = divided[3]
    column3 = divided[4]
    column1.append(uploaded_thumbs_list[-1]) # this takes the last name in the list and adds it to column1
    column2.append(uploaded_thumbs_list[column * 3]) # this takes the last but one number in the list and adds it to column2
    
else:
    column1 = divided[2]
    column2 = divided[3]
    column3 = divided[4]

#### THIS CREATES A DICTIONARY FROM amazon_links_diksh.py USING .jpg FILE NAMES AS THE KEYS

new_diksh_keys =[]

for j, k in amazon_links_diksh.items():
    j = j.replace(' ', '_')
    j = f'{j[:-1]}.jpg'.lower()
    new_diksh_keys.append(j)
 
mob_amazon_diksh = dict(zip(new_diksh_keys, list(amazon_links_diksh.values())))
mob_amazon_diksh = dict(sorted(mob_amazon_diksh.items()))


def split_dict(d, n):
    
    """Takes in a dictionary and step size to create smaller dictionaires

    Yields:
        dictionaries: Splits large dictionary into set of smaller dictionaires based on value of 'n'.
    """
    
    keys = list(d.keys())
    for i in range(0, len(keys), n):
        yield {k: d[k] for k in keys[i: i + n]}
        
gen = split_dict(mob_amazon_diksh, 10)

get_pages_list = []

for item in gen:
    get_pages_list.append(item)
    
first_page = get_pages_list[0]
inner_pages = get_pages_list[1:len(get_pages_list)-1] # list of dicts in batches of 10
last_page = get_pages_list[-1]

gs_mob_fp = jinja2.Environment(loader=jinja2.FileSystemLoader(Path(f'{cwd_path}/web_pages/templates'))).get_template('get-stuff-first-page-TEMPLATE.php').render(first_page=first_page)

gs_mob_fp_write = Path(f'{mob_web_dir}/m-get-stuff.php')

with open(gs_mob_fp_write,'w', encoding="utf-8") as mob_fp: 
    mob_fp.write(gs_mob_fp)

ftp = ftplib.FTP('ftp.jvzdesigns.com', ftp_user, ftp_pass)

ftp.cwd('./mobile/') # needs the trailing forward slash
dict_count = 0

for stuff in inner_pages:
    
    dict_count += 1
    if stuff == inner_pages[-1]:
        
        gs_mob_lp = jinja2.Environment(loader=jinja2.FileSystemLoader(Path(f'{cwd_path}/web_pages/templates'))).get_template('get-stuff-last-page-TEMPLATE.php').render(last_page=last_page)
        
        gs_mob_lp_write = Path(f'{mob_web_dir}/get-stuff-pages/gs-page{dict_count}.html')
        
        with open(gs_mob_lp_write,'w', encoding="utf-8") as mob_lp: 
            mob_lp.write(gs_mob_lp)
        
        gs_last_page = open(gs_mob_inner_write, 'rb') # file to send    
        ftp = ftplib.FTP('ftp.jvzdesigns.com', ftp_user, ftp_pass)
        ftp.cwd('./mobile/get-stuff-pages/') # needs the trailing forward slash
        ftp.storbinary(f'STOR gs-page{dict_count}.html', gs_last_page)
            
    
    else:
            
        gs_mob_inner = jinja2.Environment(loader=jinja2.FileSystemLoader(Path(f'{cwd_path}/web_pages/templates'))).get_template('get-stuff-inner-pages-TEMPLATE.php').render(stuff=stuff, dict_count=dict_count)

        gs_mob_inner_write = Path(f'{mob_web_dir}/get-stuff-pages/gs-page{dict_count}.html')

        with open(gs_mob_inner_write,'w', encoding="utf-8") as mob_inner: 
            mob_inner.write(gs_mob_inner)

        gs_inner_pages = open(gs_mob_inner_write, 'rb') # file to send    
        ftp = ftplib.FTP('ftp.jvzdesigns.com', ftp_user, ftp_pass)
        ftp.cwd('./mobile/get-stuff-pages/') # needs the trailing forward slash
        ftp.storbinary(f'STOR gs-page{dict_count}.html', gs_inner_pages)
        gs_inner_pages.close()
        print(gs_mob_inner_write)
        
get_stuff_norm = jinja2.Environment(loader=jinja2.FileSystemLoader(Path(f'{cwd_path}/web_pages/templates'))).get_template('get_stuff_3_cols_PHP-TEMPLATE.php').render(column1=column1, column2=column2, column3=column3)

get_stuff_norm_write = Path(f'{web_dir}/get-stuff.php')

with open(get_stuff_norm_write,'w', encoding="utf-8") as norm: 
        norm.write(get_stuff_norm)
    
    
ftp = ftplib.FTP('ftp.jvzdesigns.com', ftp_user, ftp_pass)
norm_versh = open(get_stuff_norm_write, 'rb') # file to send
ftp.cwd('./get-stuff/') # needs the trailing forward slash
ftp.storbinary(f'STOR get-stuff.php', norm_versh)    # send the file
norm_versh.close()

ftp = ftplib.FTP('ftp.jvzdesigns.com', ftp_user, ftp_pass)
mob_versh = open(gs_mob_fp_write, 'rb') # file to send
ftp.cwd('./mobile/') # needs the trailing forward slash
ftp.storbinary(f'STOR m-get-stuff.php', mob_versh)
mob_versh.close()                                    
ftp.quit() 
