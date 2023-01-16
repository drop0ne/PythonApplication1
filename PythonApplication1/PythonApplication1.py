import youtube_dl
from youtube_dl.utils import DownloadError
from tkinter import filedialog
from tkinter import Tk

root = Tk()
root.withdraw()

web_address = input("Please enter the web address of the video: ")

file_path = filedialog.asksaveasfilename(defaultextension=".mp4")

if not file_path:
    print("User didn't choose a location to save the video.")
    exit()

ydl_opts = {
    'outtmpl': file_path
}
try:
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([web_address])
except DownloadError as e:
    print(f"An error occurred while downloading the video: {e}")

