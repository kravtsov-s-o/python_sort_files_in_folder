import sys
from pathlib import Path

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


if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")

    arg = Path(path)
    scan(arg)

    print(f"Images: {images_files}\n")
    print(f"Videos: {videos_files}\n")
    print(f"Docs: {docs_files}\n")
    print(f"Audios: {audios_files}\n")
    print(f"Archives: {archives_files}\n")
    print(f"Other: {other_files}\n")
    print(f"Folders: {folders}\n")
    print(f"Extensions: {extensions}\n")
    print(f"Unknown Extensions: {unknown_extensions}\n")
