#!/usr/bin/python3

import os
import requests
from bs4 import BeautifulSoup, Comment

# Insp3ct0r
# link = "https://jupiter.challenges.picoctf.org/problem/44924/"

# Search source
link_2 = "http://saturn.picoctf.net:50761/"

# where are the robots
link_3 = "https://jupiter.challenges.picoctf.org/problem/60915/"

def mirror(link):
    css_files = []
    image_files = []
    script_files = []
    all_files = []

    r = requests.get(link)
    source_code = r.content + b"\n"

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
            file_path = script.attrs.get("src")
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

    with open("index.html", "wb") as index_file:
        index_file.write(source_code)

    for url in all_files:
        path = url[len(link):].split("/")
        # print(path)
        if len(path) > 1:
            pass
            file_name = path[-1]
            folders = path[:-1]
            local_path = "/".join(folders)
            # print(local_path)
            if not os.path.isdir(local_path):
                os.makedirs(local_path)
            i = requests.get(url)
            with open(f"{local_path}/{file_name}", "wb") as source_file:
                source_file.write(i.content)
        else:
            # if not os.path.isdir("WW-folder"):
            #     os.mkdir("WW-nofolder")
            i = requests.get(url)
            with open(path[0], "wb") as source_file:
                source_file.write(i.content)
    return None

def crawl_robots(link):
    disallowed = []

    robots_link = link + "robots.txt"
    # print(robots_link)
    r = requests.get(robots_link)
    robots = r.content.decode().split("\n")
    for line in robots:
        entry = line.split(" ")
        if entry[0] == "Disallow:":
            disallowed.append(entry[1])

    for path in disallowed:
        disallowed_link = link + path
        i = requests.get(disallowed_link)
        print(f"--------Disallowed entry: {path}--------")
        print(i.content.decode())
        
    return None
