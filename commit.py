import os
import shutil
from datetime import datetime
import uuid

from util import load_data, update_data
from variables import main_dir, vcs_path, data_dir  

def commit(name):
  data = load_data()
  
  if len(data["saved_files"]) < 1:
    return print("there's nothing to commit")
  
  branch = data["info"]["current_branch"]
  
  uid = uuid.uuid4().hex
  commit = os.path.join(main_dir, "vcs", "branches", data["info"]["current_branch"], "commits", str(uid))
  files = []
  
  os.mkdir(commit)
  for file in data["saved_files"]:
    if not os.path.exists(file["path"]): continue
    
    copy_path = os.path.join(commit, file["relative_path"])
    dirr = copy_path[:(copy_path.rfind("\\") + 1) or len(copy_path)]
    
    if not os.path.exists(dirr):
      os.makedirs(dirr)
      
    shutil.copyfile(file["path"], copy_path)
    
    files.append({ "real_path": file["path"], "copy_path": copy_path, "rel_path": file["relative_path"], "name": file["name"] })

  data["info"]["branches"][branch]["commits"].append({ "id": uid, "path": commit, "name": name, "files": files, "date": str(datetime.now().strftime("%d %b %Y %X")) })
  data["saved_files"] = []
  update_data(data)