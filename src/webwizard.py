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
import pywebcopy
import re
import requests

def get_files_in_dir(path_to_directory: str) -> list:
    """Accepts a path to a directory and returns a list of filepaths
    of every file in the directory.

    Dependencies:
    - os
    """
    
    list_of_files = []
    for root, dirs, files in os.walk(path_to_directory):
        for file in files:
            # append relative filepaths
            list_of_files.append(os.path.join(root,file))
    return list_of_files

def parse_for_flag(crib: str, text: str) -> list:
    """Accepts a CTF flag crib and uses it to find plaintext, rot13 encoded,
    and base64 encoded flags in given text.

    Dependencies:
    - base64
    - re
    - codecs
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

    def __init__(self, url: str, crib: str) -> None:
        self.url = url
        self.crib = crib
        pass

    def mirror_website(self, folder: str = './', robots: bool = True) -> None:
        """Download entire website at Client object's URL and parse
        source code for flag

        Dependencies:
        - pywebcopy
        """

        # name the directory that source code will be saved to
        kwargs = {
            'project_name': f"source_{self.url.strip(r'http://').strip(r'https://')}",
            'debug': False,
            'zip_project_folder': False,
            'over_write': False
        }
        # download entire website
        pywebcopy.save_website(
            url=self.url,
            project_folder=folder,
            bypass_robots=robots,
            **kwargs
        )
        concat_filepath = os.path.join(folder, kwargs['project_name'] + '.txt')
        source_filepath = os.path.join(folder, kwargs['project_name'])
        # concatenate all subfiles in website into one file to parse
        subfile_list = get_files_in_dir(source_filepath)
        for subfile in subfile_list:
            with open(subfile, 'rb') as subf:
                text = subf.read().decode('utf-8','ignore')
            with open(concat_filepath, 'a') as cfile:
                cfile.write(text)
        # parse source for flag
        with open(concat_filepath, 'rb') as f:
            text = f.read()
            parse_for_flag(self.crib, text)
        return None