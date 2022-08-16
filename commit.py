import os
import shutil
import uuid

from util import load_data
from variables import main_dir, vcs_path, data_dir  

def commit(name):
  data = load_data()
  
  uid = uuid.uuid4().hex
  commit = os.path.join(main_dir, "vcs", "branches", "main", "commits", str(uid))
  files = []
  
  os.mkdir(commit)
  for file in data["saved_files"]:
    if not os.path.exists(file["path"]): continue
    
    copy_path = os.path.join(commit, file["relative_path"])
    dirr = copy_path[:copy_path.rfind("\\") + 1]
    
    if not os.path.exists(dirr):
      os.makedirs(dirr)
      
    shutil.copyfile(file["path"], copy_path)
    
    files.append({ "real_path": file["path"], "copy_path": copy_path, "name": file["name"] })

  data["info"]["commits"].append({ "id": uid, "path": commit, "name": name, "files": files })