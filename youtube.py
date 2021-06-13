from youtube_dl import YoutubeDL
import os

audio_downloader = YoutubeDL({'format': 'bestaudio'})


def download_yt(url):
    try:
        info = audio_downloader.extract_info(url)
        filename = info['title'] + '-' + info['id'] + '.' + info['container'].split('_')[0]

        return os.getcwd() + "\\" + filename
    except Exception:
        print("Could not download song form youtube.")
