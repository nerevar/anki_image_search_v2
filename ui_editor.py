from aqt import mw
from anki.hooks import addHook

from . import shared
from . import search


def display_image(editor, i_dest_field, img_filename):
    image_tag = shared.image_tag(img_filename)
    
    editor.note.fields[i_dest_field] = image_tag
    editor.loadNote()


def search_image(editor):
    query, i_dest_field = shared.get_note_query_image_fields(editor.note)

    image_url = search.get_result_by_query(query)
    filename = shared.save_image_to_library(editor, image_url)
    if not filename:
        return

    display_image(editor, i_dest_field, filename)


def prev_image(editor):
    query, i_dest_field = shared.get_note_query_image_fields(editor.note)

    image_url = search.get_prev_result_by_query(query)
    filename = shared.save_image_to_library(editor, image_url)
    if not filename:
        return

    display_image(editor, i_dest_field, filename)


def next_image(editor):
    query, i_dest_field = shared.get_note_query_image_fields(editor.note)

    image_url = search.get_next_result_by_query(query)
    filename = shared.save_image_to_library(editor, image_url)
    if not filename:
        return

    display_image(editor, i_dest_field, filename)


def hook_image_buttons(buttons, editor):
    config = mw.addonManager.getConfig(__name__)
    query_field = config["query_field"]
    image_field = config["image_field"]

    for (cmd, func, tip, icon) in [
        ("search_image", search_image, 
            "Search for images from field '{}' to field '{}'".format(query_field, image_field), "image"),
        ("prev_image", prev_image, "Load previous image", "arrow-thick-left"),
        ("next_image", next_image, "Load next image", "arrow-thick-right"),
    ]:
        icon_path = shared.path_to("images", "{}-2x.png".format(icon))
        buttons.append(editor.addButton(icon_path, cmd, func, tip=tip))

    return buttons


def init_editor():
    addHook("setupEditorButtons", hook_image_buttons)
