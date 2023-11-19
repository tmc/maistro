import os
import re


def extract_path(text):
    # Regular expression pattern for a Linux file path
    pattern = r"/(?:[\w.-]+/)*(?:[\w.-]+|\.\.)/[\w/._-]+"

    # Search for the pattern in the string
    match = re.search(pattern, text)

    if match:
        path = match.group()
        return path
    else:
        return None


def get_script_cwd(filename=""):
    """
    Returns the absolute path of the file in the same directory as this script. (i.e. inside lib)

    Slightly hacky but works good
    """
    return os.path.join(os.path.dirname(__file__), filename)


def find_first_fext(directory, fext="png"):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if fnmatch.fnmatch(file, f"*.{fext}"):
                return os.path.join(root, file)
    return None


def find_first_png(directory):
    return find_first_fext(directory, "png")

def find_first_log(directory):
    return find_first_fext(directory, "log")

def find_first_yaml(directory):
    return find_first_fext(directory, "yaml")

def find_first_xml(directory):
    return find_first_fext(directory, "xml")

def find_first_json(directory):
    return find_first_fext(directory, "json")

