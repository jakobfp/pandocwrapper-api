import os
import sys
import time
import hashlib

from flask import send_from_directory

sys.path.append('../pandocwrapper')

import pandocwrapper

LATEX_FILES = './cis/latex'
UPLOAD_FOLDER = os.path.join(LATEX_FILES, "uploads")
ALLOWED_UPLOAD_EXT = {'tex', 'docx'}


def split_and_get_last_element(split_chr: str, string_to_split: str):
    return string_to_split.split(split_chr)[len(string_to_split.split(split_chr)) - 1]


def mkdir(directory: str):
    if not os.path.exists(directory):
        os.makedirs(directory)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_UPLOAD_EXT


def upload(file):
    if allowed_file(file.filename):
        new_dir = hashlib.sha3_224(str(time.time()).encode('utf-8')).hexdigest()
        mkdir(os.path.join(UPLOAD_FOLDER, new_dir))
        save_path = os.path.join(UPLOAD_FOLDER, new_dir, file.filename)
        file.save(save_path)
        rel_save_path = split_and_get_last_element("/latex/", save_path)
        return {"success": True, "file_path": rel_save_path, "error": ""}
    else:
        return {"success": False, "file_path": "", "error": "file not supported, please upload either .tex or .docx"}


def convert_tex(file: str, design: str, bib_file: str = None):
    path_to_files = LATEX_FILES
    if os.path.exists(os.path.join(LATEX_FILES, file)):
        template_string = design + ".tex"
        tex_converter = pandocwrapper.LatexConverter(file_in=file,
                                                     template=template_string,
                                                     path_to_files=path_to_files,
                                                     bib=bib_file)
        tex_converter.construct_command()
        result = tex_converter.convert()

        output_filename = split_and_get_last_element("/", tex_converter.file_out)

        if result is None:
            return {"success": True, "file_path": tex_converter.file_out, "file_name": output_filename, "error": ""}
        else:
            return {"success": False, "file_path": "", "file_name": "", "error": "something went wrong, check server log"}

    return {"success": False, "file_path": "", "file_name": "", "error": "file ("+file+") does not exists, please upload again"}


def download(file: str):
    # TODO: remove file after
    return send_from_directory(LATEX_FILES, file, as_attachment=True)
