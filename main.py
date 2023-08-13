import shutil
import sys

import scan
from normalize import normalize
from pathlib import Path


def handle_file(path, root_folder, new_folder):
    """
    # Move file to new folder

    :param path: Main folder for sort
    :param root_folder: path to file
    :param new_folder: new path to file
    """
    target_folder = root_folder / new_folder
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder / normalize(path.name))


def handle_archive(path, root_folder, new_folder):
    """
    Unpack archive in archives folder

    :param path: Main folder for sort
    :param root_folder: path to file
    :param new_folder: new path to folder with archive files
    :return:
    """
    target_folder = root_folder / new_folder
    target_folder.mkdir(exist_ok=True)

    new_name = normalize(path.name[:path.name.rfind('.')])

    archive_folder = target_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), str(archive_folder.resolve()))
    except shutil.ReadError:
        archive_folder.rmdir()
        return

    path.unlink()


# delete empty folders
def remove_empty_folders(path):
    """
    Delete empty folder

    :param path: path to folder
    """
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass


def get_folder_objects(root_path):
    """
    Find and remove empty folders

    :param root_path: Main folder for sort
    """
    for folder in root_path.iterdir():
        if folder.is_dir():
            remove_empty_folders(folder)
            try:
                folder.rmdir()
            except OSError:
                pass


def main(folder_path):
    """
    Start function script

    :param folder_path: folder for sort files
    """

    scan.scan(folder_path)

    for file in scan.images_files:
        handle_file(file, folder_path, 'IMAGES')

    for file in scan.videos_files:
        handle_file(file, folder_path, 'VIDEOS')

    for file in scan.docs_files:
        handle_file(file, folder_path, 'DOCUMENTS')

    for file in scan.audios_files:
        handle_file(file, folder_path, 'AUDIOS')

    # for file in scan.other_files:
    #     handle_file(file, folder_path, 'OTHERS')

    for file in scan.archives_files:
        handle_archive(file, folder_path, 'ARCHIVES')

    get_folder_objects(folder_path)


def init():
    path = sys.argv[1]
    print(f"Start in {path}")

    arg = Path(path)
    main(arg.resolve())

if __name__ == '__main__':
    init()
