from anki.utils import stripHTMLMedia

from .yimages import get_yimages


# storage of lists of images by queries
YIMAGES = {}
# indices of current image in list by queries
INDICES = {}


def get_current_image_url_by_query(query):
    query = stripHTMLMedia(query)
    if query not in YIMAGES or not YIMAGES[query] or \
            query not in INDICES or INDICES[query] < 0 or INDICES[query] >= len(YIMAGES[query]):
        return None
    return YIMAGES[query][INDICES[query]]


def get_result_by_query(query):
    query = stripHTMLMedia(query)
    if query not in YIMAGES or not len(YIMAGES[query]):
        YIMAGES[query] = get_yimages(query)

    if YIMAGES[query]:
        INDICES[query] = 0
        return get_current_image_url_by_query(query)
    else:
        INDICES[query] = -1
        return None


def get_next_result_by_query(query):
    query = stripHTMLMedia(query)
    if INDICES.get(query, -1) >= 0 and INDICES.get(query, -1) < len(YIMAGES.get(query, [])):
        INDICES[query] += 1
        return get_current_image_url_by_query(query)


def get_prev_result_by_query(query):
    query = stripHTMLMedia(query)
    if INDICES.get(query, -1) >= 1:
        INDICES[query] -= 1
        return get_current_image_url_by_query(query)
