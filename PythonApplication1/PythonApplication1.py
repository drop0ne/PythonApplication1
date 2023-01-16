import youtube_dl
from youtube_dl.utils import DownloadError
from tkinter import filedialog
from tkinter import Tk

web_address = input("Please enter the web address of the video: ")

with youtube_dl.YoutubeDL() as ydl:
    # retrieve video information
    video_info = ydl.extract_info(web_address, download=False)

    # get the available formats
    formats = video_info.get('formats', [])

    # sort formats by resolution (descending)
formats.sort(key=lambda f: int(f.get('height', 0))*int(f.get('width', 0)) if f.get('height', None) and f.get('width', None) else 0, reverse=True)

    # choose the highest resolution format
highest_resolution_format = formats[0]

    # print the chosen format's resolution
print("Chosen format's resolution:", highest_resolution_format['height'], 'x', highest_resolution_format['width'])
file_path = filedialog.asksaveasfilename(defaultextension=".mp4")
if not file_path:
    print("User didn't choose a location to save the video.")
    exit()
ydl_opts = {
    'outtmpl': file_path,
    'format': highest_resolution_format['format_id']
}
ydl.download([web_address])
