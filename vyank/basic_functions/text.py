import re

def sanitize_filename(filename):
    '''
    Windows file systems (like NTFS and FAT32) have restrictions on certain characters in file and folder names.
    Invalid Characters in Windows Filenames
    Forbidden Characters:
        < > : " / \ | ? *
        These characters have special meanings in Windows (e.g., : is used for drive letters like C:).
    Reserved Names:
        The following are reserved filenames and cannot be used as file names, even with extensions:
        CON, PRN, AUX, NUL, COM1, COM2, COM3, COM4, COM5, COM6, COM7, COM8, COM9
        LPT1, LPT2, LPT3, LPT4, LPT5, LPT6, LPT7, LPT8, LPT9
        Example: NUL.txt or COM1.mp4 are not allowed.
    Leading/Trailing Characters:
        Filenames cannot:
        End with a space ( ) or a period (.).
        Example: "example .txt" or "example." are invalid.
    Path Length Limit:
            The full path (including directories and filename) must not exceed 260 characters unless long path support is enabled.
    '''
    # Replace invalid characters with '_'
    return re.sub(r'[<>:"/\\|?*]', '_', filename)
