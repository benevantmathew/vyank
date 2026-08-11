import os
import subprocess
from pytubefix import YouTube, Playlist, Channel, Search
from pytubefix.cli import on_progress
from pytubefix.contrib.search import Filter
from vyank.basic_functions.text import sanitize_filename

class YTubeDownloader:
	def __init__(self):
		pass
	# using ffmpeg
	def merge_audio_video(self, video_path, audio_path, output_path):
		"""Merge audio and video streams using FFmpeg."""
		try:
			subprocess.run(["ffmpeg","-y","-i",video_path,"-i",audio_path,"-c","copy",output_path], check=True)
			print(f"Successfully merged: {output_path}")
		except subprocess.CalledProcessError as e:
			print(f"Error during merging: {e}")

	def download_video_highest_resolution(self, url, output_path=None):
		yt = YouTube(url, on_progress_callback=on_progress)
		title=yt.title
		title = sanitize_filename(title)
		print(f"Downloading video: {title}")

		# Download highest resolution video-only stream
		video_stream = yt.streams.filter(adaptive=True, file_extension="mp4").order_by("resolution").desc().first()
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
		except:
			pass
		print("Download complete.")

	def download_audio_only(self, url, output_path=None):
		yt = YouTube(url, on_progress_callback=on_progress)
		title=yt.title
		title = sanitize_filename(title)
		print(f"Downloading audio: {title}")
		stream = yt.streams.get_audio_only()
		stream.download(output_path=output_path)
		print("Download complete.")

	def download_playlist(self, playlist_url, output_path=None):
		pl = Playlist(playlist_url)
		title_pl=pl.title
		title_pl = sanitize_filename(title_pl)
		print(f"Downloading playlist: {title_pl}")
		for video in pl.videos:
			yt = YouTube(video.watch_url)
			title=yt.title
			title = sanitize_filename(title)
			print(f"Downloading video: {title}")

			# Download highest resolution video-only stream
			video_stream = yt.streams.filter(adaptive=True, file_extension="mp4").order_by("resolution").desc().first()
			video_path = video_stream.download(output_path=output_path)
			print(f"Video downloaded: {video_path}")

			# Download audio-only stream
			audio_stream = yt.streams.filter(only_audio=True, file_extension="mp4").first()
			audio_path = audio_stream.download(output_path=output_path)
			print(f"Audio downloaded: {audio_path}")

			# Merge video and audio
			output_file = f"{output_path}/{f'{title}_dwn'}.mp4"
			self.merge_audio_video(video_path, audio_path, output_file)
		print("Playlist download complete.")

	def download_channel_videos(self, channel_url, output_path=None):
		c = Channel(channel_url)
		print(f"Downloading videos by: {c.channel_name}")
		for video in c.videos:
			yt = YouTube(video.watch_url)
			title=yt.title
			title = sanitize_filename(title)
			print(f"Downloading video: {title}")

			# Download highest resolution video-only stream
			video_stream = yt.streams.filter(adaptive=True, file_extension="mp4").order_by("resolution").desc().first()
			video_path = video_stream.download(output_path=output_path)
			print(f"Video downloaded: {video_path}")

			# Download audio-only stream
			audio_stream = yt.streams.filter(only_audio=True, file_extension="mp4").first()
			audio_path = audio_stream.download(output_path=output_path)
			print(f"Audio downloaded: {audio_path}")

			# Merge video and audio
			output_file = f"{output_path}/{f'{title}_dwn'}.mp4"
			self.merge_audio_video(video_path, audio_path, output_file)
		print("Channel videos download complete.")

	def get_subtitles(self, url):
		yt = YouTube(url)
		title=yt.title
		title = sanitize_filename(title)
		print(f"Available subtitles for {title}:")
		return yt.captions

	def save_subtitles(self, url, lang_code, file_path):
		yt = YouTube(url)
		title=yt.title
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
