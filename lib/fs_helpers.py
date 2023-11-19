import os

def get_script_cwd(filename=""):
    """
    Returns the absolute path of the file in the same directory as this script. (i.e. inside lib)

    Slightly hacky but works good
    """
    return os.path.join(os.path.dirname(__file__), filename)