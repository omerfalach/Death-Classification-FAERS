#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import re
import lxml
import time
import shutil
import warnings
import requests
from tqdm import tqdm
from io import BytesIO
from zipfile import ZipFile
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen

# this script will find target in this list pages.
target_page = ["https://fis.fda.gov/extensions/FPD-QDE-FAERS/FPD-QDE-FAERS.html"]

# local directory to save files.
data_dir = ""

# ignore warnings
warnings.filterwarnings('ignore')


#download faers data files.
##:param faers_files: dict faers_files = {"name":"url"}
def downloadFiles(faers_files, data_dir= None):

    for file_name in tqdm(faers_files):
        try:
            print("Download " + file_name + "\t" + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            r = requests.get(faers_files[file_name], timeout=200)
            zipObject = ZipFile(BytesIO(r.content))
            listOfFileNames = zipObject.namelist()
            for fileName in listOfFileNames:
                if "DELETED" not in fileName.upper() and "TXT" in fileName.upper():
                    if data_dir == None:
                        data_dir = fileName
                    zipObject.extract(fileName, data_dir)
            print("Download " + file_name + " success!\t" + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        except Exception as e:
            print("Download " + file_name + " failed! Error: " + str(e))
        print("Sleep 30 seconds before starting download a new file.\n")
        time.sleep(30)



def get_faers_zip_files():
    print("Got web urls.\t")
    files = {}
    for page_url in target_page:
        try:
            request = urlopen(page_url)
            page_bs = BeautifulSoup(request, "lxml")
            request.close()
        except:
            request = urlopen(page_url)
            page_bs = BeautifulSoup(request)
        for url in page_bs.find_all("a"):
            a_string = str(url)
            if "ASCII" in a_string.upper():
                t_url = url.get('href')
                files[str(url.get('href'))[-16:-4]] = t_url

    # save urls to FaersFilesWebUrls.txt
    final_files = {key: files[key] for key in files if key[-4:]>='15q1'}
    save_path = os.getcwd() + "/FaersFilesWebUrls.txt"
    if (os.path.exists(save_path)):
        os.remove(save_path)
    with open(save_path, 'a+') as f:
        for k in final_files.keys():
            f.write(k + ":" + final_files[k] + "\n")
    
    print("Done!")
    return final_files


def main():
    # get faers data file's url and download them.
    faers_files = get_faers_zip_files():()
    downloadFiles(faers_files, data_dir)


if __name__ == '__main__':
    main()


# In[ ]:




