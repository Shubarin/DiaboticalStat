class ParametersException(Exception):
    pass


class ModeError(ParametersException):
    pass


class UserIdError(ParametersException):
    pass


class CountryError(ParametersException):
    pass


class CountError(ParametersException):
    pass


class ConnectException(Exception):
    pass


class UnavailableServer(ConnectException):
    pass
