import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def return_base_dir():
    return str(BASE_DIR)