import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from vyank.application.config import Config
from vyank.application.core import YTubeDownloader

class TabBase:
    """Base class for tabs in the downloader GUI."""
    def __init__(self, master, tab_name, downloader:YTubeDownloader, download_mode):
        self.downloader = downloader  # Instance of YTubeDownloader
        self.frame = tk.Frame(master, padx=10, pady=10, background="light grey")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.download_mode = download_mode  # Shared download mode variable
        self.input_string_urls = ""  # URLs to process
        self.output_folder = Config.DEFAULT_DOWNLOAD_FOLDER  # Default output folder

        # Create widgets for the tab
        self.create_widgets(tab_name)

    def create_widgets(self, tab_name):
        # YouTube URLs label and entry
        urls_label = tk.Label(self.frame, text=f"Enter {tab_name} URLs (comma-separated):")
        self.urls_entry = tk.Entry(self.frame, width=60)
        urls_label.pack(pady=10)
        self.urls_entry.pack(pady=5)

        # Output folder label and button
        output_label = tk.Label(self.frame, text="Select Output Directory:")
        self.output_entry = tk.Entry(self.frame, width=60)
        output_button = tk.Button(self.frame, text="Browse", command=self.select_output_directory)
        output_label.pack(pady=10)
        self.output_entry.pack(pady=5)
        output_button.pack(pady=5)

        # Download Mode (Video, Audio, Video & Audio)
        mode_label = tk.Label(self.frame, text="Select Download Mode:")
        mode_label.pack(pady=10)

        modes_frame = tk.Frame(self.frame, background="light grey")
        modes_frame.pack(pady=5)

        video_radio = tk.Radiobutton(
            modes_frame, text="Video", variable=self.download_mode, value="video", background="light grey"
        )
        audio_radio = tk.Radiobutton(
            modes_frame, text="Audio", variable=self.download_mode, value="audio", background="light grey"
        )
        video_audio_radio = tk.Radiobutton(
            modes_frame, text="Video and Audio", variable=self.download_mode, value="video_audio", background="light grey"
        )

        video_radio.pack(side=tk.LEFT, padx=5)
        audio_radio.pack(side=tk.LEFT, padx=5)
        video_audio_radio.pack(side=tk.LEFT, padx=5)

        # Download button
        download_button = tk.Button(self.frame, text="Download", command=self.download)
        download_button.pack(pady=20)

        # Set default output folder
        self.output_entry.insert(0, Config.DEFAULT_DOWNLOAD_FOLDER)

    def select_output_directory(self):
        self.output_folder = filedialog.askdirectory(title="Select Output Directory")
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, self.output_folder)

    def download(self):
        # Retrieve URLs and output folder
        self.input_string_urls = self.urls_entry.get().strip()
        self.output_folder = self.output_entry.get().strip()

        # Validate inputs
        if not self.input_string_urls:
            messagebox.showerror("Error", "Please enter YouTube URLs")
            return
        if not self.output_folder:
            messagebox.showerror("Error", "Please select an output directory")
            return

        # Perform download based on mode and tab type
        try:
            mode = self.download_mode.get()
            if isinstance(self, GeneralTab):
                if mode in {"video", "video_audio"}:
                    if ',' in self.input_string_urls:
                        urls=self.input_string_urls.split(',')
                        for url in urls:
                            self.downloader.download_video_highest_resolution(url, self.output_folder)
                    else:
                        self.downloader.download_video_highest_resolution(self.input_string_urls, self.output_folder)
                elif mode == "audio":
                    self.downloader.download_audio_only(self.input_string_urls, self.output_folder)
            elif isinstance(self, PlaylistTab):
                self.downloader.download_playlist(self.input_string_urls, self.output_folder, audio_only=(mode == "audio"))
            elif isinstance(self, ChannelTab):
                self.downloader.download_channel_videos(self.input_string_urls, self.output_folder, audio_only=(mode == "audio"))

            messagebox.showinfo("Success", "Download completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


class GeneralTab(TabBase):
    """General tab-specific functionality."""
    def __init__(self, master, downloader, download_mode):
        super().__init__(master, "General", downloader, download_mode)


class PlaylistTab(TabBase):
    """Playlist tab-specific functionality."""
    def __init__(self, master, downloader, download_mode):
        super().__init__(master, "Playlist", downloader, download_mode)


class ChannelTab(TabBase):
    """Channel tab-specific functionality."""
    def __init__(self, master, downloader, download_mode):
        super().__init__(master, "Channel", downloader, download_mode)