import os
import json


this_dir = os.path.dirname(os.path.abspath(__file__))
warning_messages_loc = this_dir + "/data/warning_messages.json"
output_file = os.path.abspath(this_dir + "/../output/scraped_data/warnings.json")
warnings = []
with open(warning_messages_loc) as f:
    available_warnings = json.load(f)


def issue_warning_from_exception(e, url=""):
    """ Issue a warning from an exception if such a warning exists. Otherwise, raise exception. This is to be used as
        a simple exception handler. """
    code = e.__class__.__name__
    warning = _get_warning_from_code(code)
    if warning:
        issue_warning(url, warning[code])
    else:
        raise e


def issue_warning_from_status_code(c, url=""):
    """ Issue a warning from a response's status_code if such a warning exists."""
    code = "HTTP{}".format(c)
    warning = _get_warning_from_code(code)
    if warning:
        issue_warning(url, warning[code])


def _get_warning_from_code(code):
    for w in available_warnings:
        if code in w.keys():
            return w
    return None


def issue_warning(url, message):
    new_warning = {"url": url, "message": message}
    warnings.insert(0, new_warning)  # Newest warnings should be at the front
    with open(output_file, "w") as f:
        f.write(json.dumps(warnings))
