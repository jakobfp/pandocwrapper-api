import datetime
import pandocwrapper
from const import *


def write_to_file(markdown, path):
    """
    Writes markdown to a file and saves it in a specific path.

    :param markdown: Markdown as a string
    :param path: Path to the directory where the file should be saved.

    :returns: Full path to the file.

    """
    new_dir = create_dir(parent=path)
    file_name = os.path.join(new_dir, "presentation.md")
    with open(file_name, "w") as f:
        f.write(markdown)
    return file_name


def format_markdown(slides, title_slides):
    """
    Formats slides and title_slide into a convertable markdown-string

    :param slides: Dictionary of slides: each slide has two columns (`col1` and `col2`)
    :param title_slides: Dictionary of title slides: each title slide has a `title`, `subtitle`, `author` and `date`

    :returns: The formatted markdown string.

    """
    markdown_string = ""

    if len(title_slides) > 0:
        title_slide = title_slides[0]
        markdown_string = "---\n"
        markdown_string += "title: {}\n".format(title_slide['title'] if title_slide['title'] is not "" else "Title")
        markdown_string += "subtitle: {}\n".format(title_slide['subtitle'] if title_slide['subtitle'] is not "" else "Subtitle")
        markdown_string += "author: {}\n".format(title_slide['author'] if title_slide['author'] is not "" else "Author")
        markdown_string += "date: {}\n".format(title_slide['date'] if title_slide['subtitle'] is not "" else datetime.datetime.today().strftime('%d-%m-%Y'))
        markdown_string += "---\n"

    empties = []
    for slide in slides:
        if not slide['split'] and slide['col1'] == "":
            empties.append(True)
        markdown_string += "\n# {} \n\n\n## {}\n".format(slide['title'], slide['title'])
        content = "\n{}\n\n".format(slide['col1'])
        if slide['split']:
            content = "\n\\colA{{6cm}}\n\n{}\n\n\\colB{{6cm}}\n\n{}\n\n\\colEnd\n\n".format(slide['col1'], slide['col2'])
        markdown_string += content
    if 0 < len(slides) == len(empties):
        return False
    return markdown_string


def convert(file_path, toc):
    """
    Uses the pandocwrapper module to convert a markdown-file to a PDf presentation.

    :param file_path: Path of the markdown file to be converted
    :param toc: Boolean to indicate if an outline-slide should be created or not

    :returns: Dictionary with fields, indicating if file successfully was converted and path of the output file **or** an error message if a problem occurred.

    """
    if not os.path.exists(file_path):
        return {"success": False, "file_path": file_path, "error": "{} does not exists".format(file_path)}

    rel_path = split_and_get_last_element(ROOT, file_path)[1:]
    converter = pandocwrapper.MdConverter(file_in=rel_path, path_to_files=ROOT, template=BEAMER_TEMPLATE, toc=toc)
    converter.construct_command()
    result = converter.convert()

    if result is None:
        return {"success": True, "file_path": converter.file_out, "error": ""}
    else:
        return {"success": False, "file_path": "", "error": "something went wrong, check server log"}


def create(parameters):
    """
    Takes the raw slides and title slide, formats them and converts them into a PDf presentation

    :param parameters: Dictionary with `slides`, `title_slides` and `outline`.

    :returns: Dictionary with fields, indicating if file successfully was converted and path of the output file **or** an error message if a problem occurred.

    """
    if len(parameters['titleSlides']) is 0 and len(parameters['slides']) is 0:
        return {"success": False, "file_path": "", "error": "no slides"}

    markdown = format_markdown(parameters['slides'], parameters['titleSlides'])
    if not markdown:
        return {"success": False, "file_path": "", "error": "only empty slides"}

    file_name = write_to_file(markdown, os.path.join(ROOT, UPLOAD_FOLDER))
    return convert(file_name, parameters['outline'])
