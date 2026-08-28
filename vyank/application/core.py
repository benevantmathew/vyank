import os
import subprocess
from typing import Any

from pytubefix import Channel, Playlist, Search, YouTube
from pytubefix.cli import on_progress
from pytubefix.contrib.search import Filter
from yt_dlp import YoutubeDL

from vyank.basic_functions.text import sanitize_filename


class YTubeDownloader:
    """Download YouTube media using yt-dlp by default, with pytubefix kept as an option."""

    SUPPORTED_BACKENDS = ("yt-dlp", "pytubefix")

    def __init__(self, backend="yt-dlp"):
        self.backend = self._normalize_backend(backend)

    def _normalize_backend(self, backend):
        backend = str(backend or "yt-dlp").strip().lower()
        if backend in {"yt_dlp", "ytdlp", "yt-dlp"}:
            return "yt-dlp"
        if backend in {"pytubefix", "pytube"}:
            return "pytubefix"
        raise ValueError(
            f"Unsupported download backend: {backend}. "
            f"Choose one of: {', '.join(self.SUPPORTED_BACKENDS)}"
        )

    def set_backend(self, backend):
        self.backend = self._normalize_backend(backend)

    def _get_output_path(self, output_path):
        return os.path.abspath(os.path.expanduser(output_path or os.getcwd()))

    def _yt_dlp_options(self, output_path, audio_only=False, playlist=False) -> dict[str, Any]:
        output_path = self._get_output_path(output_path)
        os.makedirs(output_path, exist_ok=True)

        if audio_only:
            download_format = "bestaudio[ext=m4a]/bestaudio/best"
        else:
            download_format = (
                "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/"
                "bestvideo+bestaudio/best"
            )

        return {
            "format": download_format,
            "outtmpl": os.path.join(output_path, "%(title).200B.%(ext)s"),
            "merge_output_format": "mp4",
            "noplaylist": not playlist,
            "windowsfilenames": True,
            "restrictfilenames": True,
        }

    def _download_with_yt_dlp(self, url, output_path=None, audio_only=False, playlist=False):
        mode = "audio" if audio_only else "video"
        print(f"Downloading with yt-dlp ({mode}): {url}")
        with YoutubeDL(self._yt_dlp_options(output_path, audio_only, playlist)) as ydl:  # type: ignore[arg-type]
            ydl.download([url])
        print("Download complete.")

    # using ffmpeg
    def merge_audio_video(self, video_path, audio_path, output_path):
        """Merge audio and video streams using FFmpeg."""
        try:
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-i",
                    video_path,
                    "-i",
                    audio_path,
                    "-c",
                    "copy",
                    output_path,
                ],
                check=True,
            )
            print(f"Successfully merged: {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error during merging: {e}")

    def download_video_highest_resolution(self, url, output_path=None):
        if self.backend == "yt-dlp":
            self._download_with_yt_dlp(url, output_path, audio_only=False, playlist=False)
            return

        yt = YouTube(url, on_progress_callback=on_progress)
        title = yt.title
        title = sanitize_filename(title)
        print(f"Downloading video with pytubefix: {title}")

        # Download highest resolution video-only stream
        video_stream = (
            yt.streams.filter(adaptive=True, file_extension="mp4")
            .order_by("resolution")
            .desc()
            .first()
        )
        video_path = video_stream.download(output_path=output_path)
        # Download audio-only stream
        audio_stream = yt.streams.filter(only_audio=True, file_extension="mp4").first()
        audio_path = audio_stream.download(output_path=output_path)
        # Merge video and audio
        output_file = f"{output_path}/{f'{title}_dwn'}.mp4"
        print(output_file)
        self.merge_audio_video(video_path, audio_path, output_file)

        # Attempt to delete the file
        try:
            os.remove(video_path)
            os.remove(audio_path)
            os.rename(output_file, f"{output_path}/{title}.mp4")
        except OSError:
            pass
        print("Download complete.")

    def download_audio_only(self, url, output_path=None):
        if self.backend == "yt-dlp":
            self._download_with_yt_dlp(url, output_path, audio_only=True, playlist=False)
            return

        yt = YouTube(url, on_progress_callback=on_progress)
        title = yt.title
        title = sanitize_filename(title)
        print(f"Downloading audio with pytubefix: {title}")
        stream = yt.streams.get_audio_only()
        stream.download(output_path=output_path)
        print("Download complete.")

    def download_video_and_audio(self, url, output_path=None):
        """Download a merged MP4 video and a separate audio-only file."""
        self.download_video_highest_resolution(url, output_path)
        self.download_audio_only(url, output_path)

    def download_playlist(self, playlist_url, output_path=None, audio_only=False, video_and_audio=False):
        if self.backend == "yt-dlp":
            if video_and_audio:
                self._download_with_yt_dlp(
                    playlist_url, output_path, audio_only=False, playlist=True
                )
                self._download_with_yt_dlp(
                    playlist_url, output_path, audio_only=True, playlist=True
                )
            else:
                self._download_with_yt_dlp(
                    playlist_url, output_path, audio_only=audio_only, playlist=True
                )
            return

        pl = Playlist(playlist_url)
        title_pl = pl.title
        title_pl = sanitize_filename(title_pl)
        print(f"Downloading playlist with pytubefix: {title_pl}")
        for video in pl.videos:
            if video_and_audio:
                self.download_video_and_audio(video.watch_url, output_path)
            elif audio_only:
                self.download_audio_only(video.watch_url, output_path)
            else:
                self.download_video_highest_resolution(video.watch_url, output_path)
        print("Playlist download complete.")

    def download_channel_videos(self, channel_url, output_path=None, audio_only=False, video_and_audio=False):
        if self.backend == "yt-dlp":
            if video_and_audio:
                self._download_with_yt_dlp(
                    channel_url, output_path, audio_only=False, playlist=True
                )
                self._download_with_yt_dlp(
                    channel_url, output_path, audio_only=True, playlist=True
                )
            else:
                self._download_with_yt_dlp(
                    channel_url, output_path, audio_only=audio_only, playlist=True
                )
            return

        c = Channel(channel_url)
        print(f"Downloading videos by pytubefix: {c.channel_name}")
        for video in c.videos:
            if video_and_audio:
                self.download_video_and_audio(video.watch_url, output_path)
            elif audio_only:
                self.download_audio_only(video.watch_url, output_path)
            else:
                self.download_video_highest_resolution(video.watch_url, output_path)
        print("Channel videos download complete.")

    def get_subtitles(self, url):
        yt = YouTube(url)
        title = yt.title
        title = sanitize_filename(title)
        print(f"Available subtitles for {title}:")
        return yt.captions

    def save_subtitles(self, url, lang_code, file_path):
        yt = YouTube(url)
        title = yt.title
        title = sanitize_filename(title)
        if lang_code in yt.captions:
            caption = yt.captions[lang_code]
            print(f"Saving subtitles for {title} in {lang_code}")
            caption.save_captions(file_path)
            print("Subtitles saved.")
        else:
            print(f"No subtitles available for language code: {lang_code}")

    def search_videos(self, query, filters=None):
        print(f"Searching for: {query}")
        s = Search(query, filters=filters)
        results = []
        for video in s.videos:
            video_info = {
                "title": video.title,
                "url": video.watch_url,
                "duration": video.length,
            }
            results.append(video_info)
        return results

    def apply_search_filters(self, **kwargs):
        filters = {}
        if "upload_date" in kwargs:
            filters["upload_date"] = Filter.get_upload_date(kwargs["upload_date"])
        if "type" in kwargs:
            filters["type"] = Filter.get_type(kwargs["type"])
        if "duration" in kwargs:
            filters["duration"] = Filter.get_duration(kwargs["duration"])
        if "features" in kwargs:
            filters["features"] = [Filter.get_features(f) for f in kwargs["features"]]
        if "sort_by" in kwargs:
            filters["sort_by"] = Filter.get_sort_by(kwargs["sort_by"])
        return filters
