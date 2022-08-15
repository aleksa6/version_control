import os
import sys
import shutil

from util import isInitialized, load_data, update_data, get_files, get_new_files, validate_args
from variables import bcolors, main_dir, vcs_path, data_dir  
  
def status():
  for file in sorted(get_files(main_dir), key=lambda file: file["isSaved"], reverse=True):
    if file["isSaved"]:
      print(bcolors.OKGREEN + file["name"] + bcolors.ENDC)
    else:
      print(bcolors.FAIL + file["name"] + bcolors.ENDC)
      
def add_files():
  pass

def add_all_files():
  # fali logika za .ignore file
  data = load_data()
  data["savedFiles"] = get_files(main_dir)
  data["savedFiles"] = list(map(lambda file : { "path": file["path"], "name": file["name"] }, data["savedFiles"]))
  update_data(data)
  
def help():
  pass

def init():
  reinit = False
  
  if os.path.exists(vcs_path):
    shutil.rmtree(vcs_path)
    reinit = True
      
  os.mkdir(vcs_path)
  os.mkdir(os.path.join(vcs_path, "snapshots"))
  os.mkdir(os.path.join(vcs_path, "data"))
  open(os.path.join(vcs_path, "data", "data.json"), "x")
  
  if reinit: print("Project reinitialized") 
  else: print("Project initialized")

def main():
    args = sys.argv
    
    if args[1] is None: help()
    elif not isInitialized and args[1] != "init": print("Project doesn't exists")
    elif args[1] == "init": init()
    elif args[1] == "status": status()
    elif args[1] == "add":
      args = sys.argv
      validate_args(args[2:])
      if args[2] == ".":
        add_all_files()
      else:
        add_files()
    
main()