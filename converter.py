import sys
sys.path.append('../pandocwrapper')
import pandocwrapper
from const import *


def convert(file: str, design: str, bib_file: str = None):
    """
    convert(file, design, bib_file)

    Converts a file (docx, odt or tex) into a PDF-file using the given design.

    :param file: Name of the file to be converted
    :param design: Name of the design that should be used. Only supports *htwberlin* so far
    :param bib_file: Name of the bibliography file, if needed. (Default is `None`)

    :returns: Dictionary with fields, indicating if file successfully was converted and path of the output file **or** an error message if a problem occurred.

    """
    if not os.path.exists(os.path.join(ROOT, file)):
        return {"success": False, "file_path": "", "file_name": "",
                "error": "file (" + file + ") does not exists, please upload again"}

    template_string = design + ".tex"
    if not os.path.exists(os.path.join(ROOT, template_string)):
        return {"success": False, "file_path": "", "file_name": "",
                "error": "(" + template_string + ") does not exists, choose another design"}

    if bib_file and not os.path.exists(os.path.join(ROOT, bib_file)):
        return {"success": False, "file_path": "", "file_name": "",
                "error": "file (" + bib_file + ") does not exists, please upload again"}

    file_type = split_and_get_last_element(".", file)
    if file_type == ODT_EXT:
        converter = pandocwrapper.OdtConverter(file_in=file,
                                               template=template_string,
                                               path_to_files=ROOT)
    elif file_type == WORD_EXT:
        converter = pandocwrapper.DocxConverter(file_in=file,
                                                template=template_string,
                                                path_to_files=ROOT)
    elif file_type == LATEX_EXT:
        resources_path = os.path.join(split_path_and_get_all_but_last_element("/", file), IMGS_FOLDER)
        print(resources_path)
        converter = pandocwrapper.LatexConverter(file_in=file,
                                                 template=template_string,
                                                 path_to_files=ROOT,
                                                 bib=bib_file,
                                                 resources_path=resources_path)
    else:
        return {"success": False, "file_path": "", "file_name": "",
                "error": "wrong file format - conversion of " + file_type + " no supported!"}

    converter.construct_command()
    result = converter.convert()

    output_filename = split_and_get_last_element("/", converter.file_out)

    if result is None:
        return {"success": True, "file_path": converter.file_out, "file_name": output_filename, "error": ""}
    else:
        return {"success": False, "file_path": "", "file_name": "", "error": "something went wrong, check server log"}



