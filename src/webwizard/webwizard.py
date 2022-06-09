#!/usr/bin/env python3
"""
A python module to aid and automate basic CTF web challenges.

Authors: John (@Magicks52), David (@DavidTimothyNam), Arya (@AryaGill)
Tested: Python 3.10.4 on Kali Linux and Python 3.9.5 on Ubuntu
"""

import base64
import bs4
import codecs
import os
import re
import requests

from urllib.parse import urljoin
from pprint import pprint


def extract_comments(source_code: str) -> list:
    """Accepts source code of a website as a string and parses comments."""

    all_comments = []
    # set up html to be parsed, find html comments
    soup = bs4.BeautifulSoup(source_code, "html.parser")
    # get html comments
    all_comments += soup.findAll(text=lambda text: isinstance(text, bs4.Comment))
    # get php, css, js, multi-line comments /* */
    all_comments += re.findall(r"/\*.+?\*/", source_code)
    # get single-line javascript comments
    all_comments += re.findall(r"//.+?$", source_code)
    return all_comments


def extract_comments_from_file(file_path: str) -> list:
    """Return a list of all comments in the file at the specified path."""

    with open(file_path, "rb") as f:
        comments = extract_comments(f.read().decode("utf-8", "ignore"))
    return comments


def get_files_in_dir(path_to_directory: str) -> list:
    """Accepts a path to a directory and returns a list of filepaths of every
    file in the directory."""

    list_of_files = []
    for root, dirs, files in os.walk(path_to_directory):
        for file in files:
            # append relative filepaths
            list_of_files.append(os.path.join(root, file))
    return list_of_files


def make_regex_string(crib: str) -> str:
    """Accepts a CTF flag crib and formats it."""

    crib = crib.strip("{")
    regex_string = ""
    for character in crib:
        regex_string += character
        regex_string += ".{0,2}"
    # regex string will match flag with any padding of less than 2 characters
    # in between each flag character (above)
    regex_string += r"\{.*?\}"
    return regex_string


def rot13_decode(enc: str) -> str:
    """Return decoded rot13 string."""
    return codecs.decode(enc, "rot-13")


def base64_decode(enc: str) -> str:
    """Return decoded base64 string."""
    return base64.b64decode(bytes(enc, "utf-8")).decode()


def format_flags(plaintext_flags: list, rot13_flags: list, base64_flags: list) -> dict:
    """Return a dictionary of decoded flags."""

    flags = {
        "plaintext": plaintext_flags,
        "rot13": list(map(rot13_decode, rot13_flags)),
        "base64": list(map(base64_decode, base64_flags)),
    }
    return flags


def parse_for_flag(crib: str, text: str) -> list:
    """Accepts a CTF flag crib and uses it to find plaintext, rot13 encoded,
    and base64 encoded flags in given text."""

    regex_string = make_regex_string(crib)
    # make regex objects from patterns for plaintext, rot13, and base64
    plaintext_pattern = re.compile(regex_string)
    rot13_pattern = re.compile(codecs.encode(regex_string, "rot-13"))
    base64_first_three = base64.b64encode(bytes(crib, "utf-8")).decode()
    base64_pattern = re.compile(
        f"{base64_first_three[0:3]}[+\\\\A-Za-z0-9]+[=]{{0,2}}\s"
    )
    # Get list of possible flags
    plaintext_flags = plaintext_pattern.findall(text)
    rot13_flags = rot13_pattern.findall(text)
    base64_flags = base64_pattern.findall(text)
    # append decoded flag with description of encoding to possible flags
    return format_flags(plaintext_flags, rot13_flags, base64_flags)


def parse_file_for_flag(crib: str, file_path: str) -> list:
    """Parses file for crib."""

    with open(file_path, "rb") as f:
        # ignore bad utf-8 characters
        flags = parse_for_flag(crib, f.read().decode("utf-8", "ignore"))
    return flags


class Wizard:
    """A class to connect to a remote server and download files."""

    def __init__(self, url: str, directory: str = "/tmp/") -> None:
        self.url = url
        self.webwizard_dir = os.path.join(directory, "webwizard_output/")

    def crawl_robots(self) -> dict:
        """Accesses robots.txt and if the page exists, returns a dictionary
        with organized information."""

        robots_link = urljoin(self.url, "robots.txt")
        r = requests.get(robots_link)
        # if the page actualy exists
        if r.status_code == 200:
            robots_info = {
                "comments": [],
                "user-agent": [],
                "disallow": [],
                "allow": [],
                "sitemap": [],
            }
            # organize the information in robots.txt
            robots = r.content.decode().split("\n")
            for line in robots:
                if "#" in line:
                    robots_info["comments"].append(line)
                else:
                    entry = line.split(" ")
                    # ignore empty entries
                    if len(entry) != 1:
                        if entry[0] == "User-agent:":
                            robots_info["user-agent"].append(entry[1])
                        elif entry[0] == "Disallow:":
                            robots_info["disallow"].append(entry[1])
                        elif entry[0] == "Allow:":
                            robots_info["allow"].append(entry[1])
                        elif entry[0] == "Sitemap:":
                            robots_info["sitemap"].append(entry[1])
        # if the page doesn't exist
        else:
            # return empty dict
            robots_info = {}
        return robots_info

    def get_comments(self) -> list:
        """Returns a list of all comments from mirrored website."""

        # get list of filepaths for each file in the folder
        subfile_list = get_files_in_dir(self.webwizard_dir)
        # parse all subfiles for comments
        comments = []
        for subfile in subfile_list:
            comments += extract_comments_from_file(subfile)
        return comments

    def get_cookies(self) -> dict:
        """Gets any cookies sent from the server from that URL. Returns a
        dictionary of all cookies received."""

        session = requests.Session()
        response = session.get(self.url)
        return session.cookies.get_dict()

    def get_all_cookies(self) -> dict:
        pass

    def get_remote_files(self, link: str) -> list:
        """Parse file at the specified link for other remote files, return a
        list of URLs to remote files."""
        css_files = []
        image_files = []
        script_files = []
        all_files = []
        # make a GET request to the website url, append \n
        # so properly ends with a newline
        r = requests.get(link)
        # set up HTML to be parsed for source files
        soup = bs4.BeautifulSoup(r.text, "html.parser")
        # find all '<link>' tags and use the path from the 'href'
        # attribute to find filepaths of css files
        for css_file in soup.find_all("link"):
            if css_file.attrs.get("href"):
                file_path = css_file.attrs.get("href")
                # if 'file_path' is not a full URL yet, append the
                # first part of the URL (the domain name)
                if "http" not in file_path:
                    file_path = urljoin(link, file_path)
                    # check to see if css file was already referenced
                    # elsewhere in the source code
                    if file_path not in css_files:
                        css_files.append(file_path)
        # find all '<img>' tags and use the path from the 'src'
        # attribute to find filepaths of image files
        for image in soup.find_all("img"):
            if image.attrs.get("src"):
                file_path = image.attrs.get("src")
                if "http" not in file_path:
                    file_path = urljoin(link, file_path)
                    if file_path not in image_files:
                        image_files.append(file_path)
        # find all '<script>' tags and use the path from the 'src'
        # attribute to find filepaths of javascript files
        for script in soup.find_all("script"):
            if script.attrs.get("src"):
                file_path = script.attrs.get("src")
                if "http" not in file_path:
                    file_path = urljoin(link, file_path)
                    if file_path not in script_files:
                        script_files.append(file_path)
        # make a list of all the URLs to all the files to download
        all_files = css_files + image_files + script_files
        return all_files

    def mirror(self) -> None:
        """Mirrors website in output directory 'webwizard_output/'."""

        # get a list of all remote files to mirror
        all_files = self.get_remote_files(self.url)
        # make 'webwizard_output/' directory
        if not os.path.isdir(self.webwizard_dir):
            os.mkdir(self.webwizard_dir)
        # function to prepend 'webwizard_output_dir'
        prepend_directory = lambda x: os.path.join(self.webwizard_dir, x)
        # make directories that mirror website structure and download
        # all files
        for url in all_files:
            path = url[len(self.url) :].split("/")
            if len(path) > 1:
                file_name = path[-1]
                # everything in the URL up to the filename
                local_path = prepend_directory("/".join(path[:-1]))
                # make directories if they don't exist
                if not os.path.isdir(local_path):
                    os.makedirs(local_path)
                # download all files
                page = requests.get(url)
                with open(f"{local_path}/{file_name}", "wb") as source_file:
                    source_file.write(page.content)
            else:
                # if the file being requested is at the root of the website,
                # write it directly to 'webwizard_output/'
                page = requests.get(url)
                with open(prepend_directory(path[0]), "wb") as source_file:
                    source_file.write(page.content)
        # download 'index.html'
        with open(prepend_directory("index.html"), "wb") as index_file:
            # make a GET request to the website url, append \n
            # so it properly ends with a newline
            r = requests.get(self.url)
            source_code = r.content + b"\n"
            index_file.write(source_code)
        return None

    def parse_website_for_flag(self, crib: str) -> list:
        """Parse mirrored website for specified crib and returns list of
        possible flags."""
        # get list of filepaths for each file in the folder
        subfile_list = get_files_in_dir(self.webwizard_dir)
        # parse all subfiles for flag
        flags = []
        for subfile in subfile_list:
            flags += parse_file_for_flag(crib, subfile)
        return flags
