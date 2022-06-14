import _module


class PyJdsException(Exception):
    """PyJds base error"""

    pass


class PyJdsAcqusitionException(PyJdsException):
    """PyJds acqusition error"""

    pass


class PyJdsConnectException(PyJdsException):
    """PyJds Connct error."""

    pass


class PyJdsStreamException(PyJdsException):
    """PyJds stream error"""

    pass



class PyJdsFeatureException(PyJdsException):
    """PyJds feature error"""

    def __init__(self, exception: _module.PyFeatureExp) -> None:
        assert isinstance(exception, _module.PyFeatureExp)
