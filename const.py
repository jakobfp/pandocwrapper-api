import os
import hashlib
import time
import shutil
from flask import send_from_directory, after_this_request


LATEX_FILES = './cis/latex'
WORD_FILES = './cis/word'
ROOT = "./cis"
UPLOAD_FOLDER = "uploads"
LATEX_EXT = 'tex'
WORD_EXT = 'docx'
ODT_EXT = 'odt'
BIB_EXT = 'bib'
JPEG_EXT = 'jpeg'
PNG_EXT = 'png'
PDF_EXT = 'pdf'
IMGS_FOLDER = 'imgs/'
BEAMER_TEMPLATE = "htwberlin-beamer.tex"
IMAGE_EXT = {JPEG_EXT, PNG_EXT, PDF_EXT}
ALLOWED_UPLOAD_EXT = {LATEX_EXT, WORD_EXT, ODT_EXT, BIB_EXT, JPEG_EXT, PNG_EXT, PDF_EXT}


def split_and_get_last_element(split_chr: str, string_to_split: str):
    """
    Get last element of a given path.

    :param split_chr: Character at which the string should be splitted
    :param string_to_split: Path to be splitted

    :returns: Last element of path.

    """
    return string_to_split.split(split_chr)[len(string_to_split.split(split_chr)) - 1]


def split_path_and_get_all_but_last_element(split_chr: str, string_to_split: str):
    """
    Get the path until a certain directory/file without the certain directory/file.

    :param split_chr: Character at which the string should be splitted
    :param string_to_split: Path to be splitted

    :returns: Path without the last element.

    """
    splitted = string_to_split.split(split_chr)[:-1]
    glued = ""
    for element in splitted:
        glued = os.path.join(glued, element)
    return glued


def mkdir(directory: str):
    """
    Create a directory if not already existing.

    :param directory: Path of the directory to be created.

    :returns: Nothing

    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def allowed_file(filename):
    """
    Check if a file is allowed to be uploaded. Allowed files are defined in :py:const:`const.ALLOWED_UPLOADED_EXT`

    :param filename: name of the file to be checked

    :returns: True/False if the files i allowed or not.

    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_UPLOAD_EXT


def create_dir(parent=None):
    """
    Create a directory with a unique name.

    If no parent is given, the parent directory will be the default upload folder: :py:const:`const.ROOT` plus :py:const:`const.UPLOAD_FOLDER`

    :param parent: the directory in which the new directory shall be created (default is None)

    :returns: The path of the new directory.

    """
    new_dir = hashlib.sha3_224(str(time.time()).encode('utf-8')).hexdigest()
    if not parent:
        parent = os.path.join(ROOT, UPLOAD_FOLDER)
    mkdir(os.path.join(parent, new_dir))
    return os.path.join(parent, new_dir)


def download(file: str):
    """
    Download a file given by path relative to :py:const:`const.ROOT`.
    Deletes the file after downloading

    :param file: Relative path of the file to be downloaded

    :returns: The file.

    """
    @after_this_request
    def remove_files(response):
        folder = split_path_and_get_all_but_last_element("/", file)
        folder_path = os.path.join(ROOT, folder)
        try:
            shutil.rmtree(folder_path)
        except OSError as e:
            print(e)
        return response

    return send_from_directory(ROOT, file, as_attachment=True)


def upload(file, path=None):
    """
    Uploads a file to an, optionally, given path.

    If no path is given, a subdirectory will be created using :py:func:`~const.create_dir`.
    If a path is given, a subdirectory inside the :py:const:`const.ROOT` directory defined in :py:mod:`const.py`. Furthermore if the file is an image defined by its extension a "imgs" directory will be created nested.

    Only files defined in :py:const:`const.ALLOWED_UPLOAD_EXT` are allowed to be uploaded.

    :param file: the file object to be uploaded
    :param path: Path to where the file should be saved (default is None)

    :returns: JSON-Object with properties, indicating if file successfully was uploaded and where **or** an error message if a problem occurred.

    """
    if not allowed_file(file.filename):
        return {"success": False, "file_path": "", "file_type": "", "error": "file not supported, please upload "
                                                                             "either .tex or .bib or .word"}
    file_type = split_and_get_last_element(".", file.filename)

    if file_type in IMAGE_EXT and path:
        mkdir(os.path.join(ROOT, split_path_and_get_all_but_last_element("/", path), IMGS_FOLDER))

    if path:
        save_path = split_path_and_get_all_but_last_element("/", path)
        save_path = os.path.join(ROOT, save_path, file.filename) \
            if file_type not in IMAGE_EXT else \
            os.path.join(ROOT, save_path, "imgs", file.filename)
    else:
        new_dir = create_dir()
        save_path = os.path.join(new_dir, file.filename)

    file.save(save_path)
    rel_save_path = split_and_get_last_element(ROOT, save_path)[1:]
    return {"success": True, "file_path": rel_save_path, "file_type": file_type, "error": ""}