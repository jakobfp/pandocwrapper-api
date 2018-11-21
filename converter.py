import sys
sys.path.append('../pandocwrapper')

import pandocwrapper


def convert(file: str, design: str, bib_file: str = None):
    template_string = design + ".tex"
    path_to_files = "../pandocwrapper/cis/latex"
    tex_converter = pandocwrapper.LatexConverter(file_in=file,
                                                 template=template_string,
                                                 path_to_files=path_to_files,
                                                 bib=bib_file)
    tex_converter.construct_command()
    tex_converter.convert()
