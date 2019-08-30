import sys
import os
import json


base_dir = os.path.dirname(sys.modules["__main__"].__file__)
warning_messages_loc = base_dir + "/crawler/data/warning_messages.json"
output_file = base_dir + "/output/meta_data/warnings.json"
warnings = []
with open(warning_messages_loc) as f:
    available_warnings = json.load(f)


def issue_warning_from_exception(e, url=""):
    e_name = e.__class__.__name__
    for w in available_warnings:
        if e_name in w.keys():
            new_warning = {"url": url, "message": w[e_name]}
            warnings.insert(0, new_warning)  # Newest warnings should be at the front
            with open(output_file, "w") as f:
                f.write(json.dumps(warnings))
            return
    raise e
