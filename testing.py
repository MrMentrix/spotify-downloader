import os

dir = {
    "X": {
        "Y": 1,
        "Z": {
            "A": 1,
            "B": 2
        }
    },
    "C": 2
}

dir_path = "/home/"

def navigate_subfolders(target, path):
    if type(target) is dict:
        print(f"{dir} is dir, path {path}")
        for key in target: 
            navigate_subfolders(target[key], os.path.join(path, key))
    
    if type(target) is int:
        print(f"{target} is int, path {path}")

navigate_subfolders(dir, dir_path)