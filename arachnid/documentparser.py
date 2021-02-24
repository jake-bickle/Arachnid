import mimetypes



def _get_matching_element(a, b):
    for x in a:
        for y in b:
            if x == y:
                return x
    return None

def parse_document_response(response, applicable_types, crawler_url):
    try:
        cd = response.headers["content-disposition"]
        file_name_start = cd.find("filename") + 10  # Get index after filename="
        file_name_end= cd.find("\"", file_name_start)
        file_name = cd[file_name_start : file_name_end]
    except KeyError:
        path = crawler_url.get_url_parts().path
        file_name = path.split("/")[-1]
    data = dict()
    data["name"] = file_name
    data["code"] = response.status_code
    possible_extensions = [t.lstrip(".") for t in mimetypes.guess_all_extensions(response.headers["content-type"])]
    data["type"] = _get_matching_element(applicable_types, possible_extensions)
    if data["type"]:
        return data 
    return None
