import os
import sys
import shutil

from util import isInitialized, load_data, update_data, get_files, get_new_files, validate_args, format_file_data
from variables import bcolors, main_dir, vcs_path, paths_to_ignore  
  
def status():
  pass
      
def add_files(files):
  data = load_data()
  filePaths = [file["path"] for file in data["savedFiles"]]
  for file in files:
    if file["path"] not in filePaths and file["path"] not in paths_to_ignore:
      print(file)
      data["savedFiles"].append(file)
      update_data(data)


def add_all_files():
  data = load_data()
  data["savedFiles"] = get_files(main_dir)
  data["savedFiles"] = list(map(lambda file : { "path": file["path"], "relative_path": file["relative_path"], "name": file["name"] }, data["savedFiles"]))
  update_data(data)
  
def help():
  pass

def init():
  reinit = False
  
  if os.path.exists(vcs_path):
    shutil.rmtree(vcs_path)
    reinit = True
      
  os.mkdir(vcs_path)
  os.makedirs(os.path.join(vcs_path, "branches", "main", "commits"))
  os.mkdir(os.path.join(vcs_path, "data"))
  open(os.path.join(vcs_path, "data", "data.json"), "x")
  
  if reinit: print("Project reinitialized") 
  else: print("Project initialized")

def main():
  args = sys.argv
  cmd = args[1]
  
  if args[1] is None: help()
  elif not isInitialized and args[1] != "init": print("Project doesn't exist yet")
  elif args[1] == "init": init()
  elif args[1] == "status": status()
  elif args[1] == "add":
    validate_args(args[2:])
    if args[2] == ".":
      add_all_files()
    else:        
      args = [format_file_data(file) for file in args[2:]]
      add_files(args)

main()