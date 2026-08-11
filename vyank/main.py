import shutil
import tkinter as tk
from tkinter import messagebox

from vyank.gui.gui import YTubeDownloaderGUI


def ensure_ffmpeg_available():
    """Return True when ffmpeg is available on PATH."""
    if shutil.which("ffmpeg"):
        return True

    messagebox.showwarning(
        "FFmpeg not found",
        "FFmpeg is required for merging video and audio downloads. "
        "Install ffmpeg and make sure it is available on PATH.",
    )
    return False


def main():
    root = tk.Tk()
    ensure_ffmpeg_available()
    YTubeDownloaderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
