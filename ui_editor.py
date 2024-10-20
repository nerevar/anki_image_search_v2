from aqt import mw
from anki.hooks import addHook

from . import utils
from . import search


def display_image(editor, img_filename, image_dest_field):
    img_tag = utils.image_tag(img_filename)

    editor.note.fields[image_dest_field] = img_tag
    editor.loadNote()


def search_image(editor):
    query = utils.get_note_query(editor.note)
    if not query:
        return

    image_url = search.get_result_by_query(query)
    if not image_url:
        utils.report("Couldn't find images for query '{}' :(".format(query))

    filename = utils.save_image_to_library(editor, image_url)
    if not filename:
        return

    display_image(editor, filename, utils.get_note_image_field_index(editor.note))


def prev_image(editor):
    query = utils.get_note_query(editor.note)
    image_url = search.get_prev_result_by_query(query)
    filename = utils.save_image_to_library(editor, image_url)
    if not filename:
        return

    display_image(editor, filename, utils.get_note_image_field_index(editor.note))


def next_image(editor):
    query = utils.get_note_query(editor.note)
    image_url = search.get_next_result_by_query(query)
    filename = utils.save_image_to_library(editor, image_url)
    if not filename:
        return

    display_image(editor, filename, utils.get_note_image_field_index(editor.note))


def hook_image_buttons(buttons, editor):
    config = utils.get_config()
    query_field = config["query_field"]
    image_field = config["image_field"]

    for (cmd, func, tip, icon) in [
        (
            "search_image",
            search_image,
            "Search for images from field '{}' to field '{}'".format(
                query_field, image_field
            ),
            "image",
        ),
        ("prev_image", prev_image, "Load previous image", "arrow-thick-left"),
        ("next_image", next_image, "Load next image", "arrow-thick-right"),
    ]:
        icon_path = utils.path_to("images", "{}-2x.png".format(icon))
        buttons.append(editor.addButton(icon_path, cmd, func, tip=tip))

    return buttons


def init_editor():
    addHook("setupEditorButtons", hook_image_buttons)
