#!/usr/bin/env python3
"""
A python module to aid and automate CTF web challenges.

Authors: John (@Magicks52), David (@DavidTimothyNam)
Tested: Python 3.9 on Kali Linux and Python _ on Ubuntu TODO: (David) fill in python and ubuntu version numbers
"""

import base64
import bs4
import codecs
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
    """A class to describe a client connected to a remote server

    Dependencies:
    - 
    """

    def __init__(self) -> None:
        pass