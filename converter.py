import os
import sys
import time
import hashlib
import shutil

from flask import send_from_directory, after_this_request

sys.path.append('../pandocwrapper')

import pandocwrapper

LATEX_FILES = './cis/latex'
WORD_FILES = './cis/word'
ROOT = "./cis"
UPLOAD_FOLDER = "uploads"
LATEX_EXT = 'tex'
WORD_EXT = 'docx'
ALLOWED_UPLOAD_EXT = {LATEX_EXT, WORD_EXT}


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


def upload(file):
    if allowed_file(file.filename):
        new_dir = hashlib.sha3_224(str(time.time()).encode('utf-8')).hexdigest()
        file_type = split_and_get_last_element(".", file.filename)
        mkdir(os.path.join(ROOT, UPLOAD_FOLDER, new_dir))
        save_path = os.path.join(ROOT, UPLOAD_FOLDER, new_dir, file.filename)
        file.save(save_path)
        rel_save_path = split_and_get_last_element(ROOT, save_path)[1:]
        return {"success": True, "file_path": rel_save_path, "file_type": file_type, "error": ""}
    else:
        return {"success": False, "file_path": "", "file_type": "", "error": "file not supported, please upload "
                                                                             "either .tex or .word"}


def convert_tex(file: str, design: str, bib_file: str = None):
    if os.path.exists(os.path.join(ROOT, file)):
        template_string = design + ".tex"
        tex_converter = pandocwrapper.LatexConverter(file_in=file,
                                                     template=template_string,
                                                     path_to_files=ROOT,
                                                     bib=bib_file)
        tex_converter.construct_command()
        result = tex_converter.convert()

        output_filename = split_and_get_last_element("/", tex_converter.file_out)

        if result is None:
            return {"success": True, "file_path": tex_converter.file_out, "file_name": output_filename, "error": ""}
        else:
            return {"success": False, "file_path": "", "file_name": "", "error": "something went wrong, check server "
                                                                                 "log"}

    return {"success": False, "file_path": "", "file_name": "", "error": "file ("+file+") does not exists, please "
                                                                                       "upload again"}


def convert_docx(file: str, design: str):
    if os.path.exists(os.path.join(ROOT, file)):
        template_string = design + ".tex"
        docx_converter = pandocwrapper.DocxConverter(file_in=file, template=template_string, path_to_files=ROOT)
        docx_converter.construct_command()
        result = docx_converter.convert()

        output_filename = split_and_get_last_element("/", docx_converter.file_out)
        if result is None:
            return {"success": True, "file_path": docx_converter.file_out, "file_name": output_filename, "error": ""}
        else:
            return {"success": False, "file_path": "", "file_name": "", "error": "something went wrong, check server "
                                                                                 "log"}

    return {"success": False, "file_path": "", "file_name": "", "error": "file ("+file+") does not exists, please "
                                                                                       "upload again"}


def download(file: str):
    # TODO: remove file after
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
