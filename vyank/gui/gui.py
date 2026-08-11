import tkinter as tk
from tkinter import ttk
from vyank.application.config import Config
from vyank.gui.tab_base import (
    GeneralTab,
    PlaylistTab,
    ChannelTab
)
from vyank.application.core import YTubeDownloader  # Import your custom downloader class


class YTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Ytube Downloader v{Config.VERSION}")
        self.root.geometry("500x500")

        # Shared download mode variable
        self.download_mode = tk.StringVar(value="video")

        # Create GUI Components
        self.create_widgets()

    def create_widgets(self):
        # Tab control
        self.tab_control = ttk.Notebook(self.root)

        # Create tabs
        self.general_tab = GeneralTab(self.tab_control, self.download_mode)
        self.playlist_tab = PlaylistTab(self.tab_control, self.download_mode)
        self.channel_tab = ChannelTab(self.tab_control, self.download_mode)

        # Add tabs to the notebook
        self.tab_control.add(self.general_tab.frame, text="General")
        self.tab_control.add(self.playlist_tab.frame, text="Playlist")
        self.tab_control.add(self.channel_tab.frame, text="Channel")

        self.tab_control.pack(expand=True, fill="both")


class YTubeDownloaderGUI:
    """Main GUI class for the YouTube Downloader."""
    def __init__(self, root):
        self.root = root
        self.root.title(f"YTube Downloader v{Config.VERSION}")
        self.root.geometry("500x500")

        # Initialize downloader and shared variables
        self.downloader = YTubeDownloader()
        self.download_mode = tk.StringVar(value="video")  # Shared download mode

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Tab control
        self.tab_control = ttk.Notebook(self.root)

        # Tabs
        self.general_tab = GeneralTab(self.tab_control, self.downloader, self.download_mode)
        self.playlist_tab = PlaylistTab(self.tab_control, self.downloader, self.download_mode)
        self.channel_tab = ChannelTab(self.tab_control, self.downloader, self.download_mode)

        self.tab_control.add(self.general_tab.frame, text="General")
        self.tab_control.add(self.playlist_tab.frame, text="Playlist")
        self.tab_control.add(self.channel_tab.frame, text="Channel")

        self.tab_control.pack(expand=True, fill="both")