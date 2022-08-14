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

def loadData():
  with open(os.path.join(data_dir, "data.json"), "r") as f:
    try :
      return json.load(f)
    except:
      return { "savedFiles": [] }

def updateData(data):
  with open(os.path.join(data_dir, "data.json"), "w") as f:
    f.write(json.dumps(data))
        
  
def getFiles(directory):
    if len(os.listdir(main_dir)) == 0: return []
    
    data = loadData()
    files = []
    for path in os.listdir(directory):
        isHidden = path.startswith(".")
        name = path
        path = os.path.join(directory, path)
        
        if os.path.isfile(path):
            isSaved = path in [file["path"] for file in data["savedFiles"]]
            files.append({ "path": path, "name": name, "isSaved": isSaved })
        elif not isHidden:
            files.extend(getFiles(path))
            
    return files

def getNewFiles(directory):
  data = loadData()
  files = []
  for file in getFiles(directory):
    if file["path"] not in [file["path"] for file in data["savedFiles"]]:
      files.append(file)
  return files
  
def status():
    for file in sorted(getFiles(main_dir), key=lambda file: file["isSaved"], reverse=True):
        if file["isSaved"]:
            print(bcolors.OKGREEN + file["name"] + bcolors.ENDC)
        else:
            print(bcolors.FAIL + file["name"] + bcolors.ENDC)

def init():
  reinit = False
  
  if os.path.exists(vcs_path):
    shutil.rmtree(vcs_path)
    reinit = True
      
  os.mkdir(vcs_path)
  os.mkdir(os.path.join(vcs_path, "snapshots"))
  os.mkdir(os.path.join(vcs_path, "data"))
  open(os.path.join(vcs_path, "data", "data.json"), "x")
      
  data = loadData()
  data["savedFiles"] = getFiles(main_dir)
  data["savedFiles"] = list(map(lambda file : { "path": file["path"], "name": file["name"] }, data["savedFiles"]))
  updateData(data)
      
  if reinit: print("Project reinitialized") 
  else: print("Project initialized")

def main():
    arg = sys.argv[1]
    
    if not isInitialized and arg != "init": print("Project doesn't exists")
    elif arg == "init": init()
    elif arg == "status": status()
    
main()