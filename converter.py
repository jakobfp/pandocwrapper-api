from flask import send_from_directory
import sys
sys.path.append('../pandocwrapper')

import pandocwrapper
import os

LATEX_FILES = './cis/latex'
UPLOAD_FOLDER = os.path.join(LATEX_FILES, "uploads")
ALLOWED_UPLOAD_EXT = {'tex', 'docx'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_UPLOAD_EXT


def upload(file):
    if allowed_file(file.filename):
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        return {"success": True}
    else:
        return {"success": False, "error": "file not supported, please upload either .tex or .docx"}


def convert(file: str, design: str, bib_file: str = None):
    path_to_files = LATEX_FILES
    file = os.path.join('uploads', file.split('\\')[len(file.split('\\'))-1])
    if os.path.exists(os.path.join(path_to_files, file)):
        template_string = design + ".tex"
        tex_converter = pandocwrapper.LatexConverter(file_in=file,
                                                     template=template_string,
                                                     path_to_files=path_to_files,
                                                     bib=bib_file)
        tex_converter.construct_command()
        result = tex_converter.convert()
        if result is None:
            return {"success": True, "file_path": tex_converter.file_out}
        else:
            return {"error": result}

    return {"error": "file ("+file+") does not exists"}


def download(file: str):
    # TODO: remove file after
    return send_from_directory(LATEX_FILES, file, as_attachment=True)
