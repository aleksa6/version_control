import os
import sys
import shutil
from turtle import update

from util import is_initialized, load_data, update_data, get_files, get_new_files, validate_args, format_file_data
from variables import bcolors, main_dir, vcs_path, paths_to_ignore  
  
def status():
  pass
      
def add_files(files):
  data = load_data()
  file_paths = [file["path"] for file in data["saved_files"]]
  for file in files:
    if file["path"] not in file_paths and file["path"] not in paths_to_ignore:
      data["saved_files"].append(file)
      update_data(data)


def add_all_files():
  data = load_data()
  data["saved_files"] = get_files(main_dir)
  data["saved_files"] = list(map(lambda file : { "path": file["path"], "relative_path": file["relative_path"], "name": file["name"] }, data["saved_files"]))
  update_data(data)
  
def help():
  pass

def branch(name):
  # os.makedirs(os.path.join(main_dir, "vcs", "branches", name))
  branches = os.listdir(os.path.join(main_dir, "vcs", "branches"))
  if name not in branches:
    data = load_data()
    data["info"]["branches"].append(name)
    
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
  data = { "saved_files": [], "info": { "branches": ["main"] } }
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
      branch("test")

main()

# filter(lambda x )