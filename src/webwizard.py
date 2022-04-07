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
    regex_string += "\\{.*?\\}"
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
    # return possible flags
    return possible_flags

class Client:
    """A class to connect to a remote server"""

    def __init__(self, url: str, crib: str) -> None:
        self.url = url
        self.crib = crib
        pass
    
    def mirror_website(self, folder: str = './', robots: bool = True) -> int:
        """Download entire website at Client object's URL and parse
        source code for flag

        Dependencies:
        - pywebcopy
        - GNU cat
        - GNU find
        """

        # name the directory that source code will be saved to
        kwargs = {'project_name': f"source_{self.url.strip(r'http://').strip(r'https://')}"}
        # download entire website
        pywebcopy.save_website(
            url=self.url,
            project_folder=folder,
            **kwargs
        )
        # concatenate all subfiles in website into one file to parse
        concat_filepath = os.path.join(folder, kwargs['project_name'] + '.txt')
        source_filepath = os.path.join(folder, kwargs['project_name'])
        os.popen(f"find {source_filepath} -type f -name '*' -exec cat {{}} + > {concat_filepath}")
        # parse source for flag
        with open(f'{concat_filepath}') as f:
            if parse_for_flag(self.crib, f.read()):
                for flag in parse_for_flag(self.crib, f.read())):
                    print(flag)
                return 0
        return 1