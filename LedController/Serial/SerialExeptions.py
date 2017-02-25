
class SerialError(Exception):
    """
    Base Serial Exception
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "[SERIAL ERROR] %s\n" % str(self.message)

    def log(self):
        ret = "%s" % str(self.message)
        if hasattr(self, "reason"):
            return "".join([ret, "\,==> %s" % str(self.reason)])
        return ret


class SerialInitialisationException(SerialError):
    def __init__(self, message, reason=None):
        self.message = message
        self.reason = reason

    def __str__(self):
        ret = "[INIT ERROR] %s\n" % str(self.message)
        if self.reason is not None:
            ret += "[REASON] %s\n" % str(self.reason)
        return ret


class SerialReadException(SerialError):
    def __init__(self, message, reason=None):
        self.message = message
        self.reason = reason

    def __str__(self):
        ret = "[READ ERROR] %s\n" % str(self.message)
        if self.reason is not None:
            ret += "[REASON] %s\n" % str(self.reason)
        return ret


class SerialPortNotOpenException(SerialError):
    def __init__(self, message, reason=None):
        self.message = message
        self.reason = reason

    def __str__(self):
        ret = "[PORT ERROR] %s\n" % str(self.message)
        if self.reason is not None:
            ret += "[REASON] %s\n" % str(self.reason)
        return ret


class SerialWriteException(SerialError):
    def __init__(self, message, reason=None):
        self.message = message
        self.reason = reason

    def __str__(self):
        ret = "[WRITE ERROR] %s\n" % str(self.message)
        if self.reason is not None:
            ret += "[REASON] %s\n" % str(self.reason)
        return ret


class SerialAcknowledgeException(SerialError):
    def __init__(self, message, reason=None):
        self.message = message
        self.reason = reason

    def __str__(self):
        ret = "[ACK ERROR] %s\n" % str(self.message)
        if self.reason is not None:
            ret += "[REASON] %s\n" % str(self.reason)
        return ret


class SerialMessageConversionException(SerialError):
    def __init__(self, message, reason=None):
        self.message = message
        self.reason = reason

    def __str__(self):
        ret = "[ACK ERROR] %s\n" % str(self.message)
        if self.reason is not None:
            ret += "[REASON] %s\n" % str(self.reason)
        return ret
