import os
import filecmp
from pickle import FALSE
cwd = os.getcwd()
files = []
added_files = ['test.txt']
main_dir = cwd
dir = os.path.join(cwd, 'vc')

def check():
    if not os.path.exists(dir):
        return 0
    return 1

def init():
    if check():
        print("vc directory already exists")
        return 1
    os.mkdir(dir)
    print("vc directory made")

def status():
    if not check():
        print("vc directory doesn't exist")
        return 0
    


    for file in os.listdir(main_dir):
     if os.path.isfile(os.path.join(main_dir, file)):
            files.append(file)
    files.remove('GIT.docx')
    files.remove('library.py')
    for file in added_files:
        files.remove(file)
    match, mismatch, errors = filecmp.cmpfiles(dir, main_dir, files, shallow= False)
    print('\033[1;32;40m', added_files)
    mismatch += errors
    print('\033[1;31;40m',mismatch)
    print('\033[0;37;40m')


status()

    






