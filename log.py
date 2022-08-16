import os
import json
import sys

from util import isInitialized, load_data, update_data, get_files, get_new_files, validate_args, format_file_data
from variables import bcolors, main_dir, vcs_path, paths_to_ignore  

commits_path = os.path.join(vcs_path, "branches", data["info"]["current_branch"])
files_in_branch = os.listdir(commits_path)
files_in_branch = os.path.join(files_in_branch, 'commits')

def log():
    for file in files_in_branch:
        print(bcolors.WARNING + file+ bcolors.ENDC ) 


def checkout(name_of_branch):
    data = load_data()
    if not name_of_branch in data["info"]['branches']:
        return 0
    data["info"]["current_branch"] = name_of_branch



