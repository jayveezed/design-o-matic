# design-o-matic
The Design-O-Matic

Basic description:

Takes a template image (see above) and applies a user selected word to create a new design (using GIMP and Python Fu), then automatically uploads to Amazon Merch and completes the entire form filling process using auto-generated SEO titles and descriptions to fill in the relevant fields. It then automatically edits the design images to make them web-friendly, creates a web page for them to be displayed on using the Jinja 2 library, and uploads everything. The only user input is vetting the verbs to be used at the start of the process.

Detailed description of Design, The O-Matic and Everything:

Disclaimer: This is my first big project using Python and I've tried to stick to conventions and use helpful descriptions etc. but I've been self taught by an idiot.

This version of the Design-O-Matic works on Windows and uploads to Amazon Merch. I've tweaked versions of the script to work on Ubuntu and the Raspberry Pi, and they do!

What it does:

Adds a new word to a base template image to create a new design.

Uploads the new design to Amazon Merch.

Automatically creates SEO titles and descriptions to fill in the relevant fields required as part of the publishing process.

Publishes the design and generates web pages to promote it on my website.

I think the script can be (relatively) easily amended to work on other Print on Demand site and the actual designs generated can be a great deal more creative and original as they are only limited by what YOU can create in GIMP.

Before running the script you need to choose how many designs you want to generate, in this case the number of verbs to add to a list. This is done at the start of the "while loop" in the design_o_matic.py file.

Initially, a timer is started to time the process. On my laptop it takes about 2 minutes for one design from start to finish. It takes less time per design when doing batches because certain processes aren't repeated. For example, a batch of 15 would take closer to 1 min 20 secs per design.

The gimp_running_chk() function then checks if GIMP is running and, if not, starts GIMP using os.startfile(gimp.exe_file_location), it then returns GIMP's Process ID. This is used later to check GIMP's CPU usage.

The while loop calls the random_verb_generator() which uses word_sorter.py to generate a random verb for the user to vet. word_sorter.py uses Pandas to filter the original list of words (a CSV file of 9659 verbs and their tenses https://github.com/monolithpl/verb.forms.dictionary/blob/master/csv/verbs-all.csv) and to remove already used or vetted words. It creates and merges data frames of just_syns.csv and used_verbs.csv which have been appended via the while loop we are in. The resulting data frame (df_dups_removed) is filtered to stop all duplication and then run through the rand_verb_generator() function.

The rand_verb_generator() checks if the randomly chosen verb has a definition using Merriam Webster Thesaurus via it's API. This check helps later as it filters out words that have no synonyms or definitions. We need synonyms and definitions to create SEO friendly keywords and descriptions.

The while loop also writes words to various files for use later (eg. to check if already uploaded or vetted). In the script these files are uploaded to my site so I could have a central place to gather and place info because I was testing the script on 3 different machines.

The ultimate aim of the while loop is to make a list of words, verified by the user, for GIMP to apply to the template image. The while loop dictates how many words the list will take before it is considered full at which point the script moves on to the next step. I've done quite a few runs of up to 15 words at one time and the program has only faltered due to outside influences(!!!) eg. Amazon suddenly asking for a Capcha when signing in.

Once we have a user-verified list of words the script looks up each word using the Miriam Webster Thesaurus API. It pulls down all the information it has for the word, which includes short definitions of what the word means and synonyms for each meaning of the word. The synonyms and descriptions are used in pre-formatted, f-string descriptions and are SEO friendly as they describe the word used in the design. Each of the verified words generates a file (in the 'blurbs' folder) that provides a Title, Brand Name, Feature One, Feature Two and Full Description ie. the information needed to fill each field when publishing designs on Amazon Merch.

After this the GIMP process kicks in. This basically involves copy and pasting the chosen words onto the base design, doing a bit of editing jiggery pokery and saving it as a new image... but there are endless possibilties to do anything you like here. I managed to write a script in GIMP's "Python Fu", and pretty chuffed about it I was as well! It applies all the changes and saves the result with specified filenames etc. I originally did this part of the process using Pyautogui (an excellent library for coding cursor movements, clicks, hotkey presses etc) and, essentially, coded every action I would take if I were creating the image manually. It worked, I just wanted to conquer Python Fu, and I flippin' well sort of did!

Like me, you might write a working script in GIMP's console but then find you can't "register" the amazing thing you spent hours learning how to write. If you have trouble registering your script to show up in GIMP you can set up a normal txt file to copy the Python Fu code from and then paste it directly into the Python Fu console in Gimp. It works, it's how the Raspberry Pi version of this works. I used Pyperclip to copy and paste. In the txt file you need to keep the Python formatting but best not to have any line spaces, until the last line, as they represent an "ENTER" command in the console.

The Design-O-Matic is now hanging on for GIMP to finish generating all the images... and we've had to go outside of the script to run the GIMP plugin which just runs inside GIMP. To determine when GIMP has finished processing everything (ie. when the Design-O-Matic can move on to the next part) the Design-O-Matic uses GIMP's Process ID that we worked out earlier in the script along with psutil.Process() to monitor GIMP's CPU usage. In my case, I set up a for loop checking cpu_percent() every 8 seconds, if it equals 0.0 GIMP has finished doing anything and the script can move on. This needed to be amended in the Ubuntu and Raspberry Pi versions of this script.

When GIMP finishes, for each verb that was selected there will be an upload-ready design in the "images" folder with title and description files inside the "blurbs" folder. Both types of files (.txt and .png) have the same name to make it easy to pair them up.

After the script calculates that GIMP has finished amazon_uploader.py is called, this uses the Selenium library to automate uploading the image/s and filling in the relevant fields at Amazon Merch. It opens a browser (I used Chrome), signs into Amazon Merch, goes to the Create page, uploads the first image in the "images" folder, fills in all the relevant naming and descriptions fields, publishes the design then moves onto the next image or, if no more images are left to upload, closes the browser.

When the uploading has finished the web_page_maker.py is started. The files that GIMP generated are large design files of print level quality.  web_page_maker.py uses the PIL library to take those design files, resize them to a web-friendly size and add a logo and black background etc. It then uses the Tinify API to compress the images so their filesize is nice and small.

The ultimate aim of web_page_maker.py is to create a web page (duh!) and upload it. I used Jinja2 which allows you to make a template html or php page and fill it up using python commands from within and outside of the template. My templates include PC and mobile versions of my web site. web_page_maker.py determines the number of images that have been uploaded altogether, creates variables based on those calculations that are then read by the templates via Jinja2. A web page of every design generated by the Design-O-Matic (401 designs at the time of writing) is uploaded using ftplib FTP.

The script then moves on from the web_page_maker.py. The files in the "images" and "blurbs" folders are uploaded to my site and also moved to the respective "UPLOADED" folders on the system, this ensures the system folders are empty and ready to use again. This is VERY IMPORTANT... the "images" and "blurbs" folders have to be emptied before running the script or your images and blurbs won't match up on Amazon Merch.

The Design-O-Matic then creats a report of what it's done and, along with the now *updated* used_verbs.csv and just_syns.csv files, uploads them so they're ready to be called on the next time the script is run.


