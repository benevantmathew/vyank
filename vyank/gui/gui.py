import tkinter as tk
from tkinter import ttk

from vyank.application.config import Config
from vyank.application.core import YTubeDownloader
from vyank.gui.tab_base import ChannelTab, GeneralTab, PlaylistTab


class YTubeDownloaderGUI:
    """Main GUI class for the YouTube Downloader."""

    def __init__(self, root):
        self.root = root
        self.root.title(f"YTube Downloader v{Config.VERSION}")
        self.root.geometry("500x540")

        # Initialize downloader and shared variables
        self.downloader = YTubeDownloader(Config.DEFAULT_DOWNLOADER_BACKEND)
        self.download_mode = tk.StringVar(value="video")  # Shared download mode
        self.download_backend = tk.StringVar(value=Config.DEFAULT_DOWNLOADER_BACKEND)

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Download engine selection at the top of the window.
        backend_frame = tk.Frame(self.root, padx=10, pady=8)
        backend_frame.pack(fill="x")

        backend_label = tk.Label(backend_frame, text="Download Engine:")
        backend_label.pack(side=tk.LEFT, padx=(0, 8))

        backend_select = ttk.Combobox(
            backend_frame,
            textvariable=self.download_backend,
            values=YTubeDownloader.SUPPORTED_BACKENDS,
            state="readonly",
            width=12,
        )
        backend_select.pack(side=tk.LEFT)
        backend_select.bind("<<ComboboxSelected>>", self.on_backend_changed)

        # Tab control
        self.tab_control = ttk.Notebook(self.root)

        # Tabs
        self.general_tab = GeneralTab(
            self.tab_control, self.downloader, self.download_mode
        )
        self.playlist_tab = PlaylistTab(
            self.tab_control, self.downloader, self.download_mode
        )
        self.channel_tab = ChannelTab(
            self.tab_control, self.downloader, self.download_mode
        )

        self.tab_control.add(self.general_tab.frame, text="General")
        self.tab_control.add(self.playlist_tab.frame, text="Playlist")
        self.tab_control.add(self.channel_tab.frame, text="Channel")

        self.tab_control.pack(expand=True, fill="both")

    def on_backend_changed(self, _event=None):
        self.downloader.set_backend(self.download_backend.get())
