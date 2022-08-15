import os
import sys
import shutil
import json

main_dir = os.getcwd()
vcs_path = os.path.join(main_dir, "vcs")
data_dir = os.path.join(main_dir, "vcs", "data")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'    
    
isInitialized = os.path.exists(os.path.join(data_dir, "data.json"))

def load_data():
  with open(os.path.join(data_dir, "data.json"), "r") as f:
    try :
      return json.load(f)
    except:
      return { "savedFiles": [] }

def update_data(data):
  with open(os.path.join(data_dir, "data.json"), "w") as f:
    f.write(json.dumps(data))
        
  
def get_files(directory):
    if len(os.listdir(main_dir)) == 0: return []
    
    data = load_data()
    files = []
    for path in os.listdir(directory):
        isHidden = path.startswith(".")
        name = path
        path = os.path.join(directory, path)
        
        if os.path.isfile(path):
            isSaved = path in [file["path"] for file in data["savedFiles"]]
            files.append({ "path": path, "name": name, "isSaved": isSaved })
        elif not isHidden:
            files.extend(get_files(path))
            
    return files

def get_new_files(directory):
  data = load_data()
  files = []
  for file in get_files(directory):
    if file["path"] not in [file["path"] for file in data["savedFiles"]]:
      files.append(file)
  return files

def validate_args(args):
  if args[0] == ".": return True
  
  for relativePath in args:
    absolutePath = os.path.join(main_dir, relativePath)
    if not (os.path.exists(absolutePath) and os.path.isfile(absolutePath)):
      return False

  return True
  
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