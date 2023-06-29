# Spotify Downloader
This script will allow you to download any music from Spotify based on links from Songs, Artists, Playlists, or Albums. SpotDL is used to locate the songs on YouTube Music and download them from there, meaning that you may not be able to download every single song you find on Spotify, even though most of them will work. You may also not be able to download any content that is excluse to Spotify, e.g., Spotify Original Podcasts.

**Legal Notice**
I take no responsibility for your usage of this script. In most countries, it will be legal to download music this way for __your own personal use__. You may not share any downloaded music, since this would be violating copyrights. This tool is meant to create your own personal and local music library for at home or on the go.

## Initial Setup
You will need to install `spotDL` and `mp3gain` onto your system. `spotDL` is a python module. You can find downloads for mp3gain [here](https://mp3gain.sourceforge.net/download.php). You can learn how to install spotdl [here](https://spotdl.github.io/spotify-downloader/installation/).

I recommend to install spotdl and run your code in a virtual environment. You can learn how to set up and activate a Python venv [here](https://docs.python.org/3/library/venv.html)

## Config
After having installed both spotDL and mp3gain, you will want to set up your personal config to ensure best possible performance.

### Selecting music to be downloaded
You want to select any Artists, Playlists, Albums, etc. you want to download. To do this, copy the link from Spotify and paste it into `urls.json`.
Here is an example:

```json
    "Michael Jackson": [
        "https://open.spotify.com/artist/3fMbdgg4jU18AjLCKBhRSm?si=dq7WvY0xTaODOKG_bInmSg"
    ]
```
The String `"Michael Jackson"` will be for your own orientation and will also be used to later create a folder called "Michael Jackson", which will help you organize your music. You can add any amount of links to such array, for example:

```json
    "Lord of the Rings": [
        "https://open.spotify.com/album/04rz93AqGy9JduzV3K81Dh?si=4ee487c74a5b46fa",
        "https://open.spotify.com/album/1zIoYLpYOq8d4HFzHJ7vc8?si=33aebf2ea4ec4765",
        "https://open.spotify.com/album/38x0H9PdY1fHh8EdfPUXqa?si=e64ef59499a24cd3"
    ]
```
This will download the soundtracks of all 3 LOTR movies and store them in the "Lord of the Rings" folder. You can turn off to use individual folders in `main.py` by setting `create_dirs = False`. However, I recommend leaving this option on, since things can turn messy quickly if you want to download a larger amount of music. The only downside to having `create_dirs = True` is that there may be rare duplicats between folders since a copy of the desired Playlists, Albums, etc. is created within each folder.

If you want an album/folder not to change any further, e.g., because it is a very large folder or it won't be updated anymore and you want to speed up the syncing process, you can add the folder's name to the `locked.json` file like this:
```json
    "locked": ["Lord of the Rings"]
```

### Sorting your URLs
The `sort_urls.py` script will sort your `urls.json` alphabetically to enhance readability and it will also ensure that you have standardized intendation.

### Threading Config
Running multiple threads at once will increase the speed at which music is downloaded and neutralized. You can select the number of threads to run for normalization in `main.py` under `max_workers = x`. The default is 4 threads. If you don't know how many threads at once your CPU can handle, look this up online. To ensure that your PC remains stable, I recommend not using more than 75% of your threads, e.g., maximum 12 threads for a 16-thread CPU.
You can select how many spotDL threads you want to run in `/path/to/.spotdl/config.json` under `"threads": x`. Since these are virtual threads, you'll be fine to use, e.g. 32 threads even if your CPU does not have as many physical threads.
You want to edit this setting since the default value is 4, which will result in rather slow downloads.

### Selecting the output directory
To select the output directory, you can change the `output_dir = "/path/to/folder"` value in `main.py`. You'll also want to select how often playlists should be updated by setting the `update_frequency = x`, which is 30 by default, meaning that after 30 days, already downloaded Playlists, Albums, Artists, etc. will be checked again.

# Have Fun!