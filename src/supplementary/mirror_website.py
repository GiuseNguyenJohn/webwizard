#!/usr/bin/python3

import os
import requests
from bs4 import BeautifulSoup, Comment


# link = "https://jupiter.challenges.picoctf.org/problem/44924/"
link_2 = "http://saturn.picoctf.net:64200/"

def find_important_files(link):
    css_files = []
    image_files = []
    script_files = []
    all_files = []

    r = requests.get(link)
    
    soup = BeautifulSoup(r.text, "html.parser")

    for css_file in soup.find_all("link"):
        if css_file.attrs.get("href"):
            file_path = css_file.attrs.get("href")
            if "http" not in file_path:
                file_path = link + file_path
                if file_path not in css_files:
                    css_files.append(file_path)

    for image in soup.find_all("img"):
        if image.attrs.get("src"):
            file_path = image.attrs.get("src")
            if "http" not in file_path:
                file_path = link + file_path
                if file_path not in image_files:
                    image_files.append(file_path)

    for script in soup.find_all("script"):
        if script.attrs.get("src"):
            file_path = image.attrs.get("src")
            if "http" not in file_path:
                file_path = link + file_path
                if file_path not in script_files:
                    script_files.append(file_path)

    all_files = css_files + image_files + script_files

    # print("----------CSS----------")
    # for file in css_files:
    #     print(file)

    # print("----------IMG----------")
    # for file in image_files:
    #     print(file)

    # print("---------JS---------")
    # for file in script_files:
    #     print(file)

    return all_files



file_paths = find_important_files(link_2)
# print(file_paths)
for url in file_paths:
    path = url[len(link_2):]
    subfolders = path.split("/")
    if not os.path.isdir(subfolders[0]): # doesn't account for multi-nested folders
        os.mkdir(subfolders[0]) 
    i = requests.get(url)
    with open(path, "wb") as source_file:
        source_file.write(i.content)
