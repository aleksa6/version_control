import os
import json
import sys

from util import  load_data, update_data, get_files, get_new_files, validate_args, format_file_data
from variables import bcolors, main_dir, vcs_path, paths_to_ignore  
data = load_data()
commits_path = os.path.join(vcs_path, "branches", data["info"]["current_branch"], "commits")
branch = data["info"]["current_branch"]
files_in_branch = data['info']["branches"][branch]["commits"]

def flog():
    for file in files_in_branch:
        # print(bcolors.WARNING + file+ bcolors.ENDC )
        print(bcolors.WARNING + file["id"] + bcolors.ENDC)
        print("Name: ", file["name"])
        print("Date: ", file["date"], "\n")

def checkout(name_of_branch):
    if not name_of_branch in data["info"]['branches']:
        return 0
    data["info"]["current_branch"] = name_of_branch
    update_data(data)



