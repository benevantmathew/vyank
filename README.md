# 🎬 vyank - YouTube Downloader

`vyank` is a small Tkinter desktop tool for downloading YouTube videos, audio, playlists, and channel videos. It uses `pytubefix` for YouTube access and `ffmpeg` for merging separate high-resolution video and audio streams into a final MP4 file.

## ✅ Features

- Simple Tkinter GUI with tabs for different download workflows
- Download a single YouTube video
- Download comma-separated video URLs from the General tab
- Download audio-only streams
- Download playlists
- Download channel videos
- Automatically sanitizes video titles for safe filenames
- Downloads to the user `Downloads` folder by default
- Uses FFmpeg to merge adaptive video-only and audio-only streams
- Packaged with a `vyank` console entry point for PyPI installation

## ⚠️ Important Notes

### YouTube Terms

Only download content that you own, are allowed to download, or are permitted to use under the content owner's terms. YouTube access behavior may change over time, so updating `pytubefix` may occasionally be required.

### FFmpeg Requirement

`vyank` needs FFmpeg for video downloads that require separate video and audio streams to be merged.

The application calls `ffmpeg` from your system `PATH`.
Check whether FFmpeg is available:

```sh
ffmpeg -version
```

## 💾 Installation

```sh
uv tool install vyank
```

For local development from this repository:

```sh
cd /path/to/vyank
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## 🚀 Usage

Launch the GUI after installation:

```sh
vyank
```

Run directly from the repository without installing:

```sh
python -m vyank.main
```

If you use the included virtual environment during development:

```sh
.venv/bin/python -m vyank.main
```

## 🖥️ GUI Workflow

### General Tab

Use the General tab for one or more normal YouTube video URLs.

1. Paste a YouTube URL into the input field.
2. For multiple videos, separate URLs with commas.
3. Choose the output directory.
4. Select the download mode:
   - `Video` downloads the highest available MP4 video stream and merges audio with FFmpeg.
   - `Audio` downloads audio only.
   - `Video and Audio` is shown in the GUI as a shared mode option, but current download handling is focused on video or audio modes.
5. Click `Download`.

### Playlist Tab

Use the Playlist tab for a YouTube playlist URL.

1. Paste the playlist URL.
2. Choose the output directory.
3. Select video or audio mode.
4. Click `Download`.

### Channel Tab

Use the Channel tab for a YouTube channel URL.

1. Paste the channel URL.
2. Choose the output directory.
3. Click `Download`.

## 📁 Default Download Folder

By default, downloads go to:

Linux/macOS:

```sh
~/Downloads
```

You can override this from the GUI by choosing another output directory.

## 📦 Project Structure

```text
vyank/
├── CHANGELOG.md
├── LICENSE
├── MANIFEST.in
├── README.md
├── pyproject.toml
└── vyank/
    ├── main.py
    ├── application/
    │   ├── config.py
    │   └── core.py
    ├── basic_functions/
    │   ├── os_funs.py
    │   └── text.py
    └── gui/
        ├── gui.py
        └── tab_base.py
```

## 🔧 Development Setup

Clone the repository:

```sh
git clone https://github.com/benevantmathew/vyank.git
cd vyank
```

Create and activate a virtual environment:

```sh
python -m venv .venv
source .venv/bin/activate
```

Install the package in editable mode:

```sh
pip install -e .
```

Install build tools when preparing a release:

```sh
pip install build twine
```

Run a quick import/compile check:

```sh
python -m compileall -q vyank
python -c "import vyank.main; print('vyank import ok')"
```

## 🧪 Build and PyPI Readiness

Build source and wheel distributions locally:

```sh
python -m build
```

Check the generated distributions:

```sh
twine check dist/*
```

Install the locally built wheel for testing:

```sh
pip install --force-reinstall dist/vyank-0.1.0-py3-none-any.whl
```

Run the installed command:

```sh
vyank
```

```sh
twine upload dist/*
```

## 📌 Package Metadata

- Package name: `vyank`
- Current version: `0.1.0`
- Python requirement: `>=3.10`
- License: MIT
- Author: Benevant Mathew
- Repository: https://github.com/benevantmathew/vyank
- Main GUI entry point: `vyank.main:main`
- Console script: `vyank`

## 🧩 Runtime Dependencies

Python packages:

- `pytubefix`

System packages:

- `ffmpeg`
- `tkinter` / Tk support for your Python installation

On some Linux distributions, Tkinter is packaged separately. If the GUI fails with a Tkinter import error, install the Tk package for your Python version.

## 📝 Changelog

See `CHANGELOG.md` for release notes.

## 📄 License

This project is licensed under the MIT License. See `LICENSE` for details.
