from predicter import eval
import sys

# "C:\Users\Fabian\Documents\GitHub\MusicGenreDetector\Britney Spears - 3.mp3"
if __name__ == "__main__":
    path = input("Enter the path to your mp3 file:")
    #path = sys.argv[1:][0]
    eval(path)
