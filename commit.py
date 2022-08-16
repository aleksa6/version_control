import os
import sys
import shutil
import json
import uuid

from util import load_data
from variables import bcolors, main_dir, vcs_path, data_dir  

def commit():
    data = load_data()
    uid = uuid.uuid4().hex
    commit = os.path.join(main_dir, "vcs", "branches", "main", "commits", str(uid))
    os.mkdir(commit)
    for file in data["saved_files"]:
        if not os.path.exists(file["path"]): continue
        shutil.copyfile(file["path"],os.path.join(commit,file["relative_path"]))
    pass