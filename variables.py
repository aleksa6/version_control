import os

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

paths_to_ignore = [
  os.path.join(main_dir, "vcs"),
  os.path.join(main_dir, "__pycache__"),
  os.path.join(main_dir, ".gitignore"),
  os.path.join(main_dir, "main.py"),
  os.path.join(main_dir, "util.py"),
  os.path.join(main_dir, "variables.py"),
  os.path.join(main_dir, "commit.py"),
  os.path.join(main_dir, "vcs.docx"),
]