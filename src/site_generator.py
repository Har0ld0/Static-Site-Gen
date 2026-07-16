import os
import shutil

def cleaning_dir(dir: str) -> None:
    if os.path.exists(dir):
        to_delete = os.listdir(dir)
        for file in to_delete:
            path = os.path.join(dir, file)
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)

def copy_to_dir(source: str, destination: str) -> None:
    if not os.path.exists(destination):
        os.mkdir(destination)

    if os.path.exists(source):
        to_copy = os.listdir(source)
        for file in to_copy:
            file_path = os.path.join(source, file)
            if os.path.isfile(file_path):
                shutil.copy(file_path, destination)
            elif os.path.isdir(file_path):
                dir_path = os.path.join(destination, file)
                copy_to_dir(file_path, dir_path)

    return None
