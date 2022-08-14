import os
cwd = os.getcwd()
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
init()




    






