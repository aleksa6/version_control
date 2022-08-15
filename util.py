import os
import json

from variables import main_dir, data_dir
  
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