import os
import json

from variables import main_dir, data_dir, paths_to_ignore
  
is_initialized = os.path.exists(os.path.join(data_dir, "data.json"))

def load_data():
  with open(os.path.join(data_dir, "data.json"), "r") as f:
    try :
      return json.load(f)
    except:
      return { "saved_files": [] }

def update_data(data):
  with open(os.path.join(data_dir, "data.json"), "w") as f:
    f.write(json.dumps(data))
  
def get_files(directory):
  if len(os.listdir(main_dir)) == 0: return []
  
  data = load_data()
  files = []
  for path in os.listdir(directory):    
    isHidden = path.startswith(".")
    if os.path.join(directory, path) in paths_to_ignore or isHidden: continue

    name = path
    path = os.path.join(directory, path)
    
    if os.path.isfile(path):
      isSaved = path in [file["path"] for file in data["saved_files"]]
      relative_path = os.path.relpath(path)
      files.append({ "path": path, "relative_path": relative_path, "name": name, "isSaved": isSaved })
    elif not isHidden:
      files.extend(get_files(path))
          
  return files

def get_new_files(directory):
  data = load_data()
  files = []
  for file in get_files(directory):
    if file["path"] in paths_to_ignore: continue
    
    if file["path"] not in [file["path"] for file in data["saved_files"]]:
      files.append(file)
  return files

def format_file_data(path):
  absolute_path = os.path.join(main_dir, path)
  relative_path = os.path.relpath(path)
  file = { "path": absolute_path, "relative_path": relative_path, "name": os.path.basename(absolute_path)}
  return file

def validate_args(args):
  if args[0] == ".": return True
  
  for relativePath in args:
    absolute_path = os.path.join(main_dir, relativePath)
    if not (os.path.exists(absolute_path) and os.path.isfile(absolute_path)):
      return False

  return True