from youtube import download_yt
import sys

# "C:\Users\Fabian\Documents\GitHub\MusicGenreDetector\Britney Spears - 3.mp3"
if __name__ == "__main__":
    # path = input("Enter the path to your mp3 file or URL from youtube:")
    if len(sys.argv[1:]) == 0:
        print("Enter the path to your mp3 file or URL from youtube as parameter")
        print("Use filename or full path for local files.")
        exit()

    from predicter import eval  # import not before here because of loading time

    path = sys.argv[1:][0]

    if path.startswith('http'):
        print('yes')

    eval(download_yt(path)) if path.startswith('http') else eval(path)
