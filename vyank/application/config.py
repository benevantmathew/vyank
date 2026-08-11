import os
from vyank.basic_functions.os_funs import get_user_profile

current_dir = os.path.abspath(os.path.dirname(__file__))
#root directory
root_dir=os.path.join(current_dir, "..")
class Config:
    USR_DIR=get_user_profile()
    VERSION=0.1
    DEFAULT_DOWNLOAD_FOLDER=os.path.join(USR_DIR,'Downloads')