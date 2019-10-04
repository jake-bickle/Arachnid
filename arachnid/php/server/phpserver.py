import subprocess as sp
import shlex
import ipaddress
import re

from . import error

valid_ip = re.compile(r'''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)''')


class PHPServer:
    """ PHPServer, despite its similarities to http.server, does not create a server on its own. It merely
        communicates with php that has been installed on the system.
    """

    def __init__(self, dir, server_address, install_loc=""):
        """
            dir is the base directory of the php files to be executed
            server_address in the form addrs:port is the address the server will run on
            install_loc is the location of the php installation where the command to execute php on the system may be
            called. If the php command can be found on the PATH environment variable, install_loc may be ignored.
        """
        self.executable_call = install_loc if install_loc else "php"
        self.dir = dir
        self.server_address = None
        self.port = None
        self.server = None
        self.stop_called = False
        self.set_ip(server_address)

    def run(self, quiet=False):
        """ Start will begin the server. It is safe to call this function on a separate thread. It will continue to run
            until either php close() is called or php terminates (likely in an error state).

            If quiet is true, it will repress the stdout
        """
        if self.is_running():
            msg = f"PHP has already started on {self.server_address}:{self.port}"
            raise error.ServerAlreadyStartedError(msg)
        self.stop_called = False
        self._open_server(quiet)
        while self.is_running() and not self.stop_called:
            self._main_loop()
        self._close_server()

    def _main_loop(self):
        pass

    def stop(self):
        """ Set a flag to safely close the server. """
        self.stop_called = True

    def kill(self):
        """ Unsafely kill the server immediately. """
        self._close_server()

    def is_running(self):
        return bool(self.server.poll() is None) if self.server else False

    def set_ip(self, ip):
        try:
            ip, port = ip.split(":")
        except ValueError:
            raise ValueError("IP must be in the form addrs:port")
        self.set_port(port)
        self.server_address = ipaddress.ip_address(ip)

    def set_port(self, port):
        self.validate_port(port)
        self.port = port

    def raise_appropriate_error(self, err):
        if "Address already in use" in err:
            raise error.AddressInUseError(err)
        else:
            raise error.PHPStdErr(err)

    # TODO Find a way to read server output as it is received
    def read_server_output(self):
        pass
        # out = self.server.stdout.readline().decode("utf-8")
        # err = self.server.stderr.readline().decode("utf-8")
        # if out != "" and not quiet:
        #     print(out)
        # if err != "":
        #     self.raise_appropriate_error(err)

    def _open_server(self, quiet=False):
        cmd = f"{self.executable_call} -S {self.server_address}:{self.port} -t {self.dir}"
        args = shlex.split(cmd)
        self.server = sp.Popen(args,
                               # stdout=sp.DEVNULL if quiet else None,
                               stderr=sp.PIPE)

    def _close_server(self):
        if self.server and self.is_running():
            self.server.terminate()

    @staticmethod
    def validate_port(port):
        msg = "Port must be an a number between 0 and 65535"
        try:
            port = int(port)
        except ValueError:
            raise ValueError(msg)
        if port < 0 or port > 65535:
            raise ValueError(msg)

    def __del__(self):
        self._close_server()
