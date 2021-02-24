import os
import json


this_dir = os.path.dirname(os.path.abspath(__file__))
# TODO Probably put this in the same directory as other files
output_file = os.path.abspath(this_dir + "/../warnings.json")  # TODO Find something to do about this
warnings = [
  {
    "SSLError": "Unable to connect securely due to missing or unsupported cipher suites. If this is your seed URL, try again with \"HTTP\" scheme rather than \"HTTPS\""
  },
  {
    "ConnectionError": "A miscellaneous connection error has occurred."
  },
  {
    "ConnectTimeout": "Connection timeout. The request timed out while trying to connect to the remote server."
  },
  {
    "ReadTimeout": "Connection timeout. Server failed to respond after 30 seconds."
  },
  {
    "UnicodeDecodeError": "Unable to decode page to utf-8."
  },
  {
    "HTTP414": "URL is too long. Server refused to respond. Arachnid has likely been caught in a bot trap."
  }
]

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
    for w in warnings:
        if code in w.keys():
            return w
    return None

def issue_warning(url, message):
    new_warning = {"url": url, "message": message}
    warnings.insert(0, new_warning)  # Newest warnings should be at the front
    with open(output_file, "w") as f:
        f.write(json.dumps(warnings))
