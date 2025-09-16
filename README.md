# Smart Video Downloader

Well well — not every project has to be serious 🙂  
This is just a small script I wrote as a hobby, mainly to download videos to listen to while working.

It goes without saying:  
 Please use this little utility **only in legal contexts** and for **videos you are allowed to download**.

---

## Installation

Clone the repository:

```bash
git clone <repo-link>
cd <repo-folder>
```

## Set up a virtual environment (recommended):

- Linux/Mac

```bash
python -m venv venv
source venv/bin/activate
```

- Windows

```bash

python -m venv venv
venv\Scripts\activate
```

## Install the dependencies:

```bash

pip install -r requirements.txt
```

## Usage

- Run the program:

```bash
python anydownload.py
```

A simple GUI window will open.
Enter a video URL or an encoded string → click Download → the download will start ✅

# Notes

Downloaded files are saved in the current working directory.

.gitignore ensures that downloaded videos are not pushed to GitHub.

This project is intended for educational and hobby purposes only.Actually for myself.
