import re
import shutil
import sys
from pathlib import Path

UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
TRANSLATION = (
    "a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t",
    "u",
    "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")
TRANS = {}

IMAGES = ('JPEG', 'PNG', 'JPG', 'SVG')
VIDEOS = ('AVI', 'MP4', 'MOV', 'MKV')
DOCUMENTS = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
AUDIOS = ('MP3', 'OGG', 'WAV', 'AMR')
ARCHIVES = ('ZIP', 'GZ', 'TAR')

images_files = list()
videos_files = list()
docs_files = list()
audios_files = list()
archives_files = list()
other_files = list()

folders = list()

extensions = set()
unknown_extensions = set()

for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()


def normalize(name):
    new_name = name.translate(TRANS)
    new_name = re.sub(r'\W', "_", new_name)

    return new_name


## SCAN

registered_extensions = {
    'IMAGES': images_files,
    'VIDEOS': videos_files,
    'DOCUMENTS': docs_files,
    'AUDIOS': audios_files,
    'ARCHIVES': archives_files
}


def get_extensions(file_name):
    """
    Get file extension

    :param file_name: File name
    :return: file extension in uppercase
    """
    return Path(file_name).suffix[1:].upper()


def scan(folder):
    """
    Scan and save in lists oll files and folders in folder

    :param folder: Path to folder which need sort
    """
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('IMAGES', 'VIDEOS', 'DOCUMENTS', 'AUDIOS', 'ARCHIVES'):
                folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)

        file_path = folder / item.name

        if not extension:
            other_files.append(file_path)
        else:
            try:
                if extension in IMAGES:
                    container = registered_extensions['IMAGES']
                    extensions_list = extensions
                elif extension in VIDEOS:
                    container = registered_extensions['VIDEOS']
                    extensions_list = extensions
                elif extension in DOCUMENTS:
                    container = registered_extensions['DOCUMENTS']
                    extensions_list = extensions
                elif extension in AUDIOS:
                    container = registered_extensions['AUDIOS']
                    extensions_list = extensions
                elif extension in ARCHIVES:
                    container = registered_extensions['ARCHIVES']
                    extensions_list = extensions
                else:
                    container = other_files
                    extensions_list = unknown_extensions

                extensions_list.add(extension)
                container.append(file_path)

            except KeyError:
                unknown_extensions.add(extension)
                other_files.append(file_path)


# MAIN
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

    scan(folder_path)

    for file in images_files:
        handle_file(file, folder_path, 'IMAGES')

    for file in videos_files:
        handle_file(file, folder_path, 'VIDEOS')

    for file in docs_files:
        handle_file(file, folder_path, 'DOCUMENTS')

    for file in audios_files:
        handle_file(file, folder_path, 'AUDIOS')

    # uncomment two next lines, if you want to remove all unknown files in a separate folder
    # and not leave them in their places

    # for file in other_files:
    #     handle_file(file, folder_path, 'OTHERS')

    for file in archives_files:
        handle_archive(file, folder_path, 'ARCHIVES')

    get_folder_objects(folder_path)


def init():
    path = sys.argv[1]
    print(f"Start in {path}")

    arg = Path(path)
    main(arg.resolve())


if __name__ == '__main__':
    init()
