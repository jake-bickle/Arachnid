class PHPServerError(Exception):
    """ Base class for all PHP server related errors"""
    pass


class ServerAlreadyStartedError(PHPServerError):
    """ Called when PHPServer.start() is called twice without PHPServer.close() """
    pass


class PHPStdErr(PHPServerError):
    """ Base class for all PHPStdErr errors"""


class AddressInUseError(PHPStdErr):
    """ Called when the IP address and port are already being used"""
