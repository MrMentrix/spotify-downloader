import subprocess
import os
import json
from datetime import datetime
import concurrent.futures

create_dirs = True

output_dir = "/path/to/folder"
update_frequency = 30 # days to wait for updating the folder again
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

os.chdir(output_dir)

for folder in urls:

    if folder in locked["locked"]:
        continue

    if folder in update_info:
        if ((datetime.now() - datetime.strptime(update_info[folder], "%d-%m-%Y %H:%M:%S")).seconds)/3600 < update_frequency * 24:
            continue

    if not os.path.exists(os.path.join(output_dir, folder)) and create_dirs:
        os.makedirs(os.path.join(output_dir, folder))

    if create_dirs:
        os.chdir(os.path.join(output_dir, folder))

    for url in urls[folder]:
        command = f'python3 -m spotdl --user-auth --overwrite skip {url}'
        subprocess.run(command, shell=True)
        
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        file_paths = [
            os.path.join(os.path.join(output_dir, folder), file)
            for file in os.listdir(os.path.join(output_dir, folder))
            if file.endswith(".mp3")
        ]
        executor.map(lambda file_path: subprocess.run(f'mp3gain -r -k "{file_path}"', shell=True), file_paths)

    update_info[folder] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    json.dump(dict(sorted(update_info.items())), open('update_info.json', 'w'), indent=4)