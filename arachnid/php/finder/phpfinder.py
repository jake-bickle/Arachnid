""" This module provides the functions to dynamically locate the PHP server executable on the current system. If it
    cannot be found, it will prompt the user for the location and save it. If this file ever gets moved, it'll prompt
    the user once again.
"""
import subprocess
import platform
import os.path

this_dir = os.path.dirname(os.path.abspath(__file__))
saved_php_path_file = os.path.join(this_dir, "saved_php_path.txt")
linux_defaults = ["/usr/bin/php"]
windows_defaults = [r"c:\php\php.exe",
                    r"c:\windows\php.exe"]


def get_php_path():
    path = check_saved_path()
    if not path:
        path = check_path_environment_variable()
    if not path:
        path = check_default_path()
    if not path:
        path = prompt_for_php_path()
    return path


def is_php_launcher(file_loc):
    """ Returns whether the file_loc is the PHP launcher.
    """
    args = f"{file_loc} -v".split()
    stdout = get_subproc_output(args)
    stdout_lines = stdout.split('\n')
    return "PHP" in stdout_lines[0] and "The PHP Group" in stdout_lines[1]


def prompt_for_php_path():
    path = None
    print("Arachnid was unable to automatically locate the PHP server on the system.")
    while not path:
        path = input("Please enter the location of the PHP launcher on your system: ").strip()
        path = path if is_php_launcher(path) else None
        if not path:
            print("\nThe PHP server was not found at that location.")
    save_path(path)
    return path


def check_saved_path():
    with open(saved_php_path_file, "r") as f:
        path = f.read()
    if path:
        return path if is_php_launcher(path) else None
    return None


def check_path_environment_variable():
    return "php" if is_php_launcher("php") else None


def check_default_path():
    op_sys = platform.system()
    if "windows" in op_sys.lower():
        default_paths = windows_defaults
    else:
        default_paths = linux_defaults
    for path in default_paths:
        if is_php_launcher(path):
            return path
    return None


def get_subproc_output(args):
    try:
        proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate("", 2)
    except subprocess.TimeoutExpired:
        return None
    except FileNotFoundError:
        return None
    if err:
        return None
    return out.decode('utf-8')


def save_path(file_loc):
    with open(saved_php_path_file, "w") as f:
        f.write(file_loc)
