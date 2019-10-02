import subprocess as sp
import shlex
import ipaddress
import re

from . import error

valid_ip = re.compile(r'''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)''')


class PHPServer:
    """ PHPServer, despite its similarities to http.server, does not create a server on its own. It merely
        communicates with php that has been installed on the system.

        Handle with care. If a close() is not called after a start(), the php server will continue to serve even after
        the end of the program!
    """

    def __init__(self, dir, server_address, port, install_loc=""):
        """
            dir is the base directory of the php files to be executed
            server_address is the IP that the server will run on
            port is the port the of the IP that the server will run on
            install_loc is the location of the php installation where the command to execute php on the system may be
            called. If the php command can be found on the PATH environment variable, install_loc may be ignored.
        """
        self.executable_call = install_loc if install_loc else "php"
        self.dir = dir
        self.server_address = None
        self.set_ip(server_address)
        self.port = port
        self.has_started = False
        self.server = None

    def start(self):
        if self.has_started:
            msg = f"PHP has already started on {self.server_address}:{self.port}"
            raise error.ServerAlreadyStartedError(msg)
        cmd = f"{self.executable_call} -S {self.server_address}:{self.port} -t {self.dir}"
        args = shlex.split(cmd)
        self.server = sp.Popen(args,
                               stdout=sp.PIPE,
                               stderr=sp.PIPE)
        self.check_for_error()
        self.has_started = True

    def close(self):
        if not self.has_started:
            self.server.terminate()
            self.server = None

    def set_ip(self, ip):
        self.server_address = ipaddress.ip_address(ip)

    def set_port(self, port):
        if port < 0 or port > 65535:
            raise error.InvalidPortError(port)
        self.port = port

    def check_for_error(self):
        out, err = self.server.communicate()
        err = err.decode("utf-8")
        if err:
            if "Address already in use" in err:
                raise error.AddressInUseError(err)
            else:
                raise error.PHPStdErr(err)
