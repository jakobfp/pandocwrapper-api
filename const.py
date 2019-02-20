import os
import hashlib
import time

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
IMAGE_EXT = {JPEG_EXT, PNG_EXT, PDF_EXT}
ALLOWED_UPLOAD_EXT = {LATEX_EXT, WORD_EXT, ODT_EXT, BIB_EXT, JPEG_EXT, PNG_EXT, PDF_EXT}


def split_and_get_last_element(split_chr: str, string_to_split: str):
    return string_to_split.split(split_chr)[len(string_to_split.split(split_chr)) - 1]


def split_path_and_get_all_but_last_element(split_chr: str, string_to_split: str):
    splitted = string_to_split.split(split_chr)[:-1]
    glued = ""
    for element in splitted:
        glued = os.path.join(glued, element)
    return glued


def mkdir(directory: str):
    if not os.path.exists(directory):
        os.makedirs(directory)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_UPLOAD_EXT


def create_dir(parent=None):
    new_dir = hashlib.sha3_224(str(time.time()).encode('utf-8')).hexdigest()
    if not parent:
        parent = os.path.join(ROOT, UPLOAD_FOLDER)
    mkdir(os.path.join(parent, new_dir))
    return os.path.join(parent, new_dir)

