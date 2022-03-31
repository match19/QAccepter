import os, fnmatch
def path(pattern):
    pattern = pattern + ".*"
    path = os.getcwd()
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                return root+"/"+name
