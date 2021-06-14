#!/usr/bin/python
from youtube import download_yt
import sys
import warnings
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

warnings.filterwarnings('ignore')

# "C:\Users\Fabian\Documents\GitHub\MusicGenreDetector\Britney Spears - 3.mp3"
if __name__ == "__main__":
    print('MUSIC-GENRE-DETECTOR'.center(40, '#'))
    print('by Daniel Zimmermann, Thomas Burri, Fabian Zbinden'.center(10, '_'))
    if len(sys.argv[1:]) == 0:
        print("Enter the path to your mp3 file or URL from youtube as parameter")
        print("Use filename or full path for local files.")
        exit()

    from predicter import eval  # import not before here because of loading time

    path = sys.argv[1:][0]

    eval(download_yt(path)) if path.startswith('http') else eval(path)
    input("Press any key to exit...")
