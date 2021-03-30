from requests.exceptions import SSLError, ConnectionError, ConnectTimeout, ReadTimeout

def handle_exception(e, url=""):
    """ Prints a warning from an exception if such a warning exists. Otherwise, raise exception. This is to be used as
        a simple exception handler. """
    exception_type = type(e)
    msg = f"Warning ({url}): "
    if exception_type == SSLError:
        msg += "Unable to connect securely due to missing or unsupported cipher suites. If this is your seed URL, try again with \"HTTP\" scheme rather than \"HTTPS\""
    elif exception_type == ConnectionError:
        msg += "A miscellaneous connection error has occurred."
    elif exception_type == ConnectTimeout: 
        msg += "Connection timeout. The request timed out while trying to connect to the remote server."
    elif exception_type == ReadTimeout: 
        msg += r"Connection timeout. Server failed to respond after {e.timeout} seconds."
    elif exception_type == UnicodeDecodeError: 
        msg += "Unable to decode page to utf-8."
    else:
        # Cannot safely recover from this exception.
        raise e
    print(msg)
