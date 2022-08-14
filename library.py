import os
import filecmp
from pickle import FALSE
cwd = os.getcwd()
files = []
added_files = []
main_dir = cwd
dir = os.path.join(cwd, 'vc')

def check():
    if not  os.path.exists(dir):
        print("vc directory doesn't exist")
        return 0
    return 1

def add_to_files():
    for file in os.listdir(main_dir):
         if os.path.isfile(os.path.join(main_dir, file)):
            if file not in files and file not in added_files:
                files.append(file)

    files.remove('GIT.docx')
    files.remove('library.py')
    

def init():
    if os.path.exists(dir):
        print("vc directory already exists")
        return 1
    os.mkdir(dir)
    print("vc directory made")

def status():
    check()

    add_to_files()
    
    match, mismatch, errors = filecmp.cmpfiles(dir, main_dir, files, shallow= False)
    added_files_for_print = list(set(added_files) - set(match))
    print('\033[1;32;40m', added_files_for_print )
    mismatch += errors
    print('\033[1;31;40m',mismatch)
    print('\033[0;37;40m')


def add(file):
    check()
    add_to_files()
    
    if file in files and file not in added_files:
        added_files.append(file)
        files.remove(file)
        print('File ', file, ' staged for commit')
        return 0
    
    elif file in added_files:
        print('File ', file, ' already staged for commit')
        return 0
    
    print("File doesn't exist" )

f = 'test.txt'
add(f)
status()

    






