import subprocess
import os
import json
from datetime import datetime
import concurrent.futures
import logging

logging.basicConfig(level=logging.INFO)

create_dirs = True

output_dir = "/home/mentrix/Music"
update_frequency = 14 # days to wait for updating the folder again
max_workers = 6

if not os.path.exists("./update_info.json"):
    with open('update_info.json', 'w') as update_file:
        json.dump({}, update_file, indent=4)

with open('update_info.json', 'r') as update_file:
    update_info = json.load(update_file)

with open('urls.json', 'r') as url_file:
    urls = json.load(url_file)

with open('locked.json', 'r') as locked_file:
    locked = json.load(locked_file)

def create_folder(path=None):
    if path is None:
        logging.info(f"Path is None")
        return

    if os.path.exists(path):
        logging.info(f"Path {path} already exists")
        return

    try:
        os.makedirs(path)
        return
    except Exception as e:
        logging.ERROR(e)

def download_songs(url, path):
    os.chdir(path)
    command = f"python3 -m spotdl --user-auth --overwrite skip {url}"

    logging.info(f"Running command {command} in {path}")

    subprocess.run(command, shell=True)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        file_paths = [os.path.join(path,  file) for file in os.listdir(path) if file.endswith(".mp3")]
        executor.map(lambda file_path: subprocess.run(f'mp3gain -r -k "{file_path}"', shell=True), file_paths)

def navigate_subfolder(target, path):
    if type(target) is dict:
        logging.info(f"{target} is dir, path {path}")
        for key in target:
            navigate_subfolder(target[key], os.path.join(path, key))
        return
    
    if type(target) is list:
        logging.info(f"{target} is list, path {path}")
        
        if not os.path.exists(path):
            logging.info(f"Creating new folder/path {path}")
            create_folder(path)
        
        for url in target:
            logging.info(f"Downloading from {url}")
            download_songs(url, path)
        return

    print(f"Target is type {type(target)}")

for folder in urls:

    if folder in locked["locked"]:
        continue

    if folder in update_info:
        if ((datetime.now() - datetime.strptime(update_info[folder], "%d-%m-%Y %H:%M:%S")).seconds)/3600 < update_frequency * 24:
            continue

    path = os.path.join(output_dir, folder)
    logging.info(f"Navigating subfolder: {path}")
    navigate_subfolder(urls[folder], path)

    update_info[folder] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    json.dump(dict(sorted(update_info.items())), open('update_info.json', 'w'), indent=4)