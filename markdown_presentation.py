import sys
sys.path.append('../pandocwrapper')

import pandocwrapper
from const import *


def write_to_file(markdown, path):
    new_dir = create_dir(parent=path)
    file_name = os.path.join(new_dir, "presentation.md")
    with open(file_name, "w") as f:
        f.write(markdown)
    return file_name


def format_markdown(slides, title_slides):
    markdown_string = ""

    if len(title_slides) > 0:
        title_slide = title_slides[0]
        markdown_string = "---\n"
        markdown_string += "title: {}\n".format(title_slide['title'])
        markdown_string += "subtitle: {}\n".format(title_slide['subtitle'])
        markdown_string += "author: {}\n".format(title_slide['author'])
        markdown_string += "date: {}\n".format(title_slide['date'])
        markdown_string += "---\n"

    for slide in slides:
        markdown_string += "\n## {}\n".format(slide['title'])
        content = "\n{}\n\n".format(slide['col1'])
        if slide['split']:
            content = "\n\\colA{{6cm}}\n\n{}\n\n\\colB{{6cm}}\n\n{}\n\n\\colEnd\n\n".format(slide['col1'], slide['col2'])
        markdown_string += content

    return markdown_string


def convert(file_path):
    if not os.path.exists(file_path):
        return {"success": False, "file_path": file_path, "error": "{} does not exists".format(file_path)}

    rel_path = split_and_get_last_element(ROOT, file_path)[1:]
    converter = pandocwrapper.MdConverter(file_in=rel_path, path_to_files=ROOT, template=BEAMER_TEMPLATE)
    converter.construct_command()
    result = converter.convert()

    if result is None:
        return {"success": True, "file_path": converter.file_out, "error": ""}
    else:
        return {"success": False, "file_path": "", "error": "something went wrong, check server log"}


def create(all_slides):

    if len(all_slides['titleSlides']) is 0 and len(all_slides['slides']) is 0:
        return {"success": False, "file_path": "", "error": "no slides"}

    markdown = format_markdown(all_slides['slides'], all_slides['titleSlides'])
    file_name = write_to_file(markdown, os.path.join(ROOT, UPLOAD_FOLDER))
    return convert(file_name)
