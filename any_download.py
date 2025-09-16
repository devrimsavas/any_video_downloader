import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import yt_dlp
import base64

#  decode av-style encrypted URLs
def try_decrypt_av(encoded: str) -> str:
    try:
        reversed_str = encoded[::-1]
        base64_decoded = base64.b64decode(reversed_str).decode()
        key = "K9L"
        out = ''
        for i, char in enumerate(base64_decoded):
            r = key[i % 3]
            decoded_char = chr(ord(char) + (ord(r) % 5 + 1))
            out += decoded_char
        final_url = base64.b64decode(out).decode()
        return final_url
    except Exception:
        return encoded  # return original if decoding fails

def download_video(url, log_box):
    log_box.insert(tk.END, f"Downloading: {url}\n")
    log_box.see(tk.END)

    class MyLogger:
        def debug(self, msg): pass
        def warning(self, msg):
            log_box.insert(tk.END, f"[Warning] {msg}\n")
            log_box.see(tk.END)
        def error(self, msg):
            log_box.insert(tk.END, f"[Error] {msg}\n")
            log_box.see(tk.END)
        def info(self, msg):
            log_box.insert(tk.END, msg + "\n")
            log_box.see(tk.END)

    def progress_hook(d):
        if d['status'] == 'downloading':
            downloaded = d.get('_percent_str', '').strip()
            speed = d.get('_speed_str', '').strip()
            eta = d.get('_eta_str', '').strip()
            line = f"Downloading: {downloaded} at {speed}, ETA {eta}\n"
            log_box.insert(tk.END, line)
            log_box.see(tk.END)
        elif d['status'] == 'finished':
            log_box.insert(tk.END, f" GREAT..  Downloaded: {d['filename']}\n")
            log_box.see(tk.END)

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': True,
        'retries': 5,
        'fragment_retries': 5,
        'logger': MyLogger(),
        'progress_hooks': [progress_hook],
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        log_box.insert(tk.END, "****** All done!\n")
    except Exception as e:
        log_box.insert(tk.END, f" Download failed: {e}\n")
    log_box.see(tk.END)

def on_download_click(entry, log_box):
    raw_input = entry.get().strip()
    if not raw_input:
        messagebox.showwarning("Input Error", "Please enter a video URL.")
        return

    # Try decode, fallback to original
    url = try_decrypt_av(raw_input)

    threading.Thread(target=download_video, args=(url, log_box)).start()

def create_gui():
    window = tk.Tk()
    window.title("Any Video Downloader")
    window.geometry("640x420")

    tk.Label(window, text="Enter Video URL or Encoded String:").pack(pady=10)
    url_entry = tk.Entry(window, width=90)
    url_entry.pack()

    log_area = scrolledtext.ScrolledText(window, width=80, height=18)
    log_area.pack(padx=10, pady=10)

    download_button = tk.Button(window, text="Download", command=lambda: on_download_click(url_entry, log_area))
    download_button.pack(pady=10)

    window.mainloop()

create_gui()
