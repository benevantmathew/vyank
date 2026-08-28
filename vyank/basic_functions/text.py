import re
import unicodedata


WINDOWS_RESERVED_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    "COM1",
    "COM2",
    "COM3",
    "COM4",
    "COM5",
    "COM6",
    "COM7",
    "COM8",
    "COM9",
    "LPT1",
    "LPT2",
    "LPT3",
    "LPT4",
    "LPT5",
    "LPT6",
    "LPT7",
    "LPT8",
    "LPT9",
}


def sanitize_filename(filename):
    """
    Return a safe filename stem using only base ASCII letters, numbers,
    spaces, hyphens, and underscores.

    Unicode symbols and punctuation from video titles are removed. Accented
    letters are normalized to their base ASCII form where possible.
    """
    filename = str(filename or "download")

    # Normalize accented letters to their base form and drop non-ASCII symbols.
    filename = unicodedata.normalize("NFKD", filename)
    filename = filename.encode("ascii", "ignore").decode("ascii")

    # Keep only base letters/numbers and simple filename separators.
    filename = re.sub(r"[^A-Za-z0-9 _-]+", " ", filename)
    filename = re.sub(r"\s+", " ", filename).strip(" ._-")

    if not filename:
        filename = "download"

    if filename.upper() in WINDOWS_RESERVED_NAMES:
        filename = f"{filename}_file"

    return filename[:200]
