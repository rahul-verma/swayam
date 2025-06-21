import os
from pathlib import Path

def is_absolute_path(path):
    return Path(path).is_absolute()

class TextFile:
    
    def __init__(self, path):
        if is_absolute_path(path):
            self.__path = path
        else:
            self.__path = os.path.join(os.environ["PROJECT_PATH"], "data", "file", path)
        with open(self.__path, "r") as f:
            self.__text = f.read()

    @property
    def text(self):
        return self.__text