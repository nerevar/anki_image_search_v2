import os
from os.path import dirname, abspath, realpath
import urllib
import importlib
from tempfile import mkstemp

from aqt import mw


CURRENT_DIR = dirname(abspath(realpath(__file__)))


def path_to(*args):
    return os.path.join(CURRENT_DIR, *args)


def get_config():
    return mw.addonManager.getConfig(__name__)


def get_note_query(note):
    field_names = mw.col.models.fieldNames(note.model())    
    query_field_name = get_config().get("query_field", "")
    
    if query_field_name in field_names:
        query_field = field_names.index(query_field_name)
        return note.fields[query_field]
    
    if importlib.util.find_spec("aqt"):
        from aqt.utils import showWarning
        showWarning(f"Field '{query_field_name}' is absent, please check addon settings. Existing fields: {field_names}", title="Anki Image Search v2 Addon")

    return None


def get_note_image_field_index(note):
    field_names = mw.col.models.fieldNames(note.model())

    return field_names.index(get_config()["image_field"])


def save_file_to_library(editor, image_url, prefix, suffix):
    (i_file, temp_path) = mkstemp(prefix=prefix, suffix=suffix)

    with urllib.request.urlopen(image_url) as response:
        image_binary = response.read()

    os.write(i_file, image_binary)
    os.close(i_file)

    result_filename = editor.mw.col.media.addFile(temp_path)
    try:
        os.unlink(temp_path)
    except:
        pass
    return result_filename


def save_image_to_library(editor, image_url):
    if not image_url:
        return
    # parsing Yandex Images thumbnail url to get id
    image_id = image_url.split("id=")[1].split("&")[0]
    return save_file_to_library(editor, image_url, image_id, ".webp")


def image_tag(image_url):
    attrs = {"src": image_url, "class": "imgsearch"}

    tag_components = ['{}="{}"'.format(key, val) for key, val in attrs.items()]

    return "<img " + " ".join(tag_components) + " />"


def report(text):
    if importlib.util.find_spec("aqt"):
        from aqt.utils import showWarning

        showWarning(text, title="Anki Image Search v2 Addon")
    else:
        print(text)
