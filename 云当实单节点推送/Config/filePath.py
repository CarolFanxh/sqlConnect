import os

def get_current_directory():
    cur_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
    return cur_dir
