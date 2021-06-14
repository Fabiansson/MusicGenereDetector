#!/usr/bin/python
from youtube import download_yt
import sys
import warnings
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

warnings.filterwarnings('ignore')

# "C:\Users\Fabian\Documents\GitHub\MusicGenreDetector\Britney Spears - 3.mp3"
if __name__ == "__main__":
    title = '''  __  __           _       _____                     _____       _            _                    __   ___  
 |  \/  |         (_)     / ____|                   |  __ \     | |          | |                  /_ | / _ \ 
 | \  / |_   _ ___ _  ___| |  __  ___ _ __  _ __ ___| |  | | ___| |_ ___  ___| |_ ___  _ __  __   _| || | | |
 | |\/| | | | / __| |/ __| | |_ |/ _ \ '_ \| '__/ _ \ |  | |/ _ \ __/ _ \/ __| __/ _ \| '__| \ \ / / || | | |
 | |  | | |_| \__ \ | (__| |__| |  __/ | | | | |  __/ |__| |  __/ ||  __/ (__| || (_) | |     \ V /| || |_| |
 |_|  |_|\__,_|___/_|\___|\_____|\___|_| |_|_|  \___|_____/ \___|\__\___|\___|\__\___/|_|      \_/ |_(_)___/ 
'''
    print(title)
    print('by Daniel Zimmermann, Thomas Burri, Fabian Zbinden'.center(10, '_'))
    if len(sys.argv[1:]) == 0:
        print("Enter the path to your mp3 file or URL from youtube as parameter")
        print("Use filename or full path for local files.")
        exit()

    from predicter import eval  # import not before here because of loading time

    path = sys.argv[1:][0]

    eval(download_yt(path)) if path.startswith('http') else eval(path)
    input("Press any key to exit...")
