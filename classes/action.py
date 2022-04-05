import os, fnmatch
def get_action_file(pattern):
    pattern = pattern + ".*"
    path = os.path.dirname(os.path.realpath(__file__))
    path = path + "/../action"
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                return root+"/"+name
