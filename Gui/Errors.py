

class MyException(Exception):
    pass


class SerialReadException(MyException):
    pass


class SerialBufferOverflowException(MyException):
    pass