import youtube_dl
from youtube_dl.utils import DownloadError
from tkinter import filedialog

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class ProgressBarWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="ProgressBar Demo")
        self.set_border_width(10)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.progressbar = Gtk.ProgressBar()
        vbox.pack_start(self.progressbar, True, True, 0)

    def update_progress(self, progress_percentage):
        self.progressbar.set_fraction(progress_percentage)
        self.progressbar.set_text(str(progress_percentage))

class Downloader:
    def __init__(self):
        self.ydl_opts = {}

    def download(self, url, save_path):
        self.ydl_opts['outtmpl'] = save_path
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([url])

class Video:
    def __init__(self, url):
        self.url = url
        self.ydl = youtube_dl.YoutubeDL()
        self.video_info = self.ydl.extract_info(self.url, download=False)
        self.formats = self.video_info.get('formats', [])
        self.formats.sort(key=lambda f: int(f.get('height', 0))*int(f.get('width', 0)) if f.get('height', None) and f.get('width', None) else 0, reverse=True)
        self.highest_resolution_format = self.formats[0]

    def get_format(self):
        return self.highest_resolution_format

def progress_hook(d):
    if d['status'] == 'downloading':
        win.update_progress(d["_percent_str"])

win = ProgressBarWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()

web_address = input("Please enter the web address of the video: ")
video = Video(web_address)

file_path = filedialog.asksaveasfilename(defaultextension=".mp4")
if not file_path:
    print("User didn't choose a location to save the video.")
    exit()

video_format = video.get_format()
downloader = Downloader()
downloader.ydl_opts = {'format': video_format['format_id'], 'progress_hooks': [progress_hook]}

downloader.download(web_address, file_path)
Gtk.main()
