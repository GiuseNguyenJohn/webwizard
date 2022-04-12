#!/usr/bin/env python3
"""
A python module to aid and automate CTF web challenges.

Authors: John (@Magicks52), David (@DavidTimothyNam)
Tested: Python 3.9 on Kali Linux and Python _ on Ubuntu TODO: (David) fill in python and ubuntu version numbers
"""

import base64
import bs4
import codecs
import os
import re
import requests

def get_files_in_dir(path_to_directory: str) -> list:
    """Accepts a path to a directory and returns a list of filepaths
    of every file in the directory.
    """
    
    list_of_files = []
    for root, dirs, files in os.walk(path_to_directory):
        for file in files:
            # append relative filepaths
            list_of_files.append(os.path.join(root,file))
    return list_of_files

def mirror(link: str, folder: str = './') -> None:
    """Accepts URL and mirrors website in output file named 'webwizard_output/'."""
    # TODO: allow user to choose which dir to mirror website to
    # TODO: output to webwizard_output/
    css_files = []
    image_files = []
    script_files = []
    all_files = []
    # make a GET request to the website url, append \n to
    # TODO: (David) mention why you're appending \n
    r = requests.get(link)
    source_code = r.content + b"\n"
    # create bs4 object
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    # find all '<link>' tags and use the path from the 'href'
    # attribute to find filepaths of css files
    for css_file in soup.find_all("link"):
        if css_file.attrs.get("href"):
            file_path = css_file.attrs.get("href")
            # if 'file_path' is not a full URL yet, append the
            # first part of the URL (the domain name)
            if "http" not in file_path:
                file_path = link + file_path
                # check to see if css file was already referenced
                # elsewhere in the source code
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

def parse_for_flag(crib: str, text: str) -> list:
    """Accepts a CTF flag crib and uses it to find plaintext, rot13 encoded,
    and base64 encoded flags in given text.
    """

    crib = crib.strip("{")
    regex_string = ""
    for character in crib:
        regex_string += character
        regex_string += ".{0,2}"
    # regex string will match flag with any padding of less than 2 characters
    # in between each flag character (above)
    regex_string += r"\{.*?\}"
    # Pattern of plaintext, rot13, and base64
    plaintext_pattern = re.compile(regex_string)
    rot13_pattern = re.compile(codecs.encode(regex_string, 'rot-13'))
    base64_first_three = base64.b64encode(bytes(crib, 'utf-8')).decode()
    base64_pattern = re.compile(f"{base64_first_three[0:3]}[+\\\\A-Za-z0-9]+[=]{{0,2}}\s")
    # Get list of possible flags
    possible_flags = []
    plaintext_flags = plaintext_pattern.findall(text)
    rot13_flags = rot13_pattern.findall(text)
    base64_flags = base64_pattern.findall(text)
    # append decoded flag with description of encoding to possible flags
    if plaintext_flags:
        possible_flags += ["plaintext flag: {}".format(x) for x in plaintext_flags]
    if rot13_flags:
        possible_flags += ["rot13 flag: {}".format(codecs.decode(x, 'rot-13')) for x in rot13_flags]
    if base64_flags:
        possible_flags += ["base64 flag: {}".format(base64.b64decode(bytes(x, 'utf-8')).decode()) for x in base64_flags]
    # print possible flags and exit
    if possible_flags:
        for flag in possible_flags:
            print(flag)
        exit(0)
    exit(1)

class Client:
    """A class to connect to a remote server"""

    def __init__(self, url: str) -> None:
        self.url = url

    def mirror_and_parse(self, crib: str, folder: str = './') -> None:
        """Download entire website at Client object's URL and parse
        source code for flag
        """

        # mirror website locally
        mirror(self.url, folder)
        # define name of directory with mirrored files and file to 
        # concatenate to
        source_filepath = os.path.join(folder, 'webwizard_output/')
        concat_filepath = os.path.join(folder, 'concatenated_output.txt')
        # get list of filepaths for each file
        subfile_list = get_files_in_dir(source_filepath)
        # concatenate all subfiles in website into one file to parse
        for subfile in subfile_list:
            with open(subfile, 'rb') as subf:
                text = subf.read().decode('utf-8','ignore')
            with open(concat_filepath, 'a') as cfile:
                cfile.write(text)
        # parse source for flag
        with open(concat_filepath) as f:
            text = f.read()
            parse_for_flag(crib, text)
        return None