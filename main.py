import os
import sys
import shutil
import random
import filecmp
from datetime import datetime
import uuid

from util import is_initialized, load_data, update_data, get_files, validate_args, format_file_data
from variables import bcolors, main_dir, vcs_path, paths_to_ignore  
from commit import commit
  
def status():
  data = load_data()
  branch = data["info"]["current_branch"]
  
  commits = data["info"]["branches"][branch]["commits"]

  if len(commits) < 1:
    for file in data["saved_files"]:
      print(bcolors.OKGREEN + "new file:         " + file["name"] + bcolors.ENDC)
    for file in get_files(main_dir):
      if file["path"] not in [file["path"] for file in data["saved_files"]]:
        print(bcolors.FAIL + "untracked:        " + file["name"] + bcolors.ENDC)
    return
  
  commons = [file["name"] for file in commits[-1]["files"]]
  
  for file in get_files(main_dir):
    if file["name"] not in commons:
      if file["path"] in [data["path"] for data in data["saved_files"]]:
        print(bcolors.OKGREEN + "new file:         " + file["name"] + bcolors.ENDC)
      else:
        print(bcolors.FAIL + "untracked:        " + file["name"] + bcolors.ENDC)
  
  match, missmatch, errors = filecmp.cmpfiles(main_dir, commits[-1]["path"], commons)

  for filename in match:
    print(bcolors.OKGREEN + "up to date:       " + file["name"] + bcolors.ENDC)
  for filename in missmatch:
    print(bcolors.FAIL + "modified:         " + filename + bcolors.ENDC)
  for filename in errors:
    print(bcolors.FAIL + "deleted:          " + filename + bcolors.ENDC)

def add_files(files):
  data = load_data()
  file_paths = [file["path"] for file in data["saved_files"]]
  for file in files:
    if file["path"] not in file_paths and file["path"] not in paths_to_ignore and os.path.exists(file["path"]) and os.path.isfile(file["path"]):
      data["saved_files"].append(file)
      update_data(data)
    else:
      print("Could not add " + file["name"] + " to staging area")


def add_all_files():
  data = load_data()
  data["saved_files"] = get_files(main_dir)
  data["saved_files"] = list(map(lambda file : { "path": file["path"], "relative_path": file["relative_path"], "name": file["name"] }, data["saved_files"]))
  update_data(data)

get_branches = lambda : os.listdir(os.path.join(main_dir, "vcs", "branches"))

def log_branches():
  data = load_data()
  for branch in get_branches():
    if branch == data["info"]["current_branch"]:
      print("*" + bcolors.OKGREEN + branch + bcolors.ENDC)
    else:
      print(branch)

def create_branch(names):
  data = load_data()
  branches = get_branches()
  for name in names:
    if name.isalpha() and name not in branches:
      os.makedirs(os.path.join(main_dir, "vcs", "branches", name, "commits"))
      data["info"]["branches"][name] = { "commits": [] }
  update_data(data)
  
def checkout(name_of_branch):
  data = load_data()
  if not name_of_branch in data["info"]['branches']:
    return print("Branch not found")
  data["info"]["current_branch"] = name_of_branch
  update_data(data)

def merge(b1, b2 = "main"):
  data = load_data()
  b1commits = data["info"]["branches"][b1]["commits"]
  b2commits = data["info"]["branches"][b2]["commits"]
  
  if len(b1commits) < 1 or len(b2commits) < 1:
    return print("there are no commits in one of the branches you specified")
  
  commons = []
  for i in range(len(b1commits[-1]["files"])):
    file = b1commits[-1]["files"][i]
    if file["real_path"] in [file["real_path"] for file in b2commits[-1]["files"]]:
      rand = random.randint(0, 2)
      file1 = [x for x in b2commits[-1]["files"] if x["real_path"] == file["real_path"]][0]
      file2 = [x for x in b1commits[-1]["files"] if x["real_path"] == file["real_path"]][0]
      if os.path.getsize(file1["copy_path"]) > os.path.getsize(file2["copy_path"]):
        commons.append(file1)  
      else:
        commons.append(file2)  

  for file in commons:
    dirr = file["real_path"][:(file["real_path"].rfind("\\") + 1) or len(file["real_path"])]
    if not os.path.exists(dirr):
      os.makedirs(dirr)
    shutil.copyfile(file["copy_path"], file["real_path"])

  for file in b1commits[-1]["files"]:
    if file["real_path"] not in [file["real_path"] for file in commons]:
      dirr = file["real_path"][:(file["real_path"].rfind("\\") + 1) or len(file["real_path"])]
      if not os.path.exists(dirr):
        os.makedirs(dirr)
      shutil.copyfile(file["copy_path"], file["real_path"])

  for file in b2commits[-1]["files"]:
    if file["real_path"] not in [file["real_path"] for file in commons]:
      dirr = file["real_path"][:(file["real_path"].rfind("\\") + 1) or len(file["real_path"])]
      if not os.path.exists(dirr):
        os.makedirs(dirr)
      shutil.copyfile(file["copy_path"], file["real_path"])
    
def init():
  reinit = False
  
  if os.path.exists(vcs_path):
    shutil.rmtree(vcs_path)
    reinit = True
      
  os.mkdir(vcs_path)
  os.makedirs(os.path.join(vcs_path, "branches", "main", "commits"))
  os.mkdir(os.path.join(vcs_path, "data"))
  open(os.path.join(vcs_path, "data", "data.json"), "x")
  
  data = load_data()
  data = { "saved_files": [], "info": { "branches": { "main": {"commits": [] } }, "current_branch": "main"  } }
  update_data(data)
  
  if reinit: print("Project reinitialized") 
  else: print("Project initialized")

def main():
  args = sys.argv
  cmd = args[1]
  
  if cmd is None: help()
  elif not is_initialized and cmd != "init": print("Project doesn't exist yet")
  elif cmd == "init": init()
  elif cmd == "status": status()
  elif cmd == "add":
    validate_args(args[2:])
    if args[2] == ".":
      add_all_files()
    else:        
      args = [format_file_data(file) for file in args[2:]]
      add_files(args)
  elif cmd == "branch":
    if len(args) < 3:
      log_branches()
    else:
      create_branch(args[2:])
  elif cmd == "commit":
    if len(args) < 3: return print("You have to specify name of the commit")
    commit(args[2])
  elif cmd == "checkout":
    if len(args) < 3:
      return print("You have to specify name of the branch")
    checkout(args[2])
  elif cmd == "merge":
    merge(args[2], args[3])
    

main()

# filter(lambda x )