from json import JSONDecodeError

'''
failure type exceptions
these exceptions will mark test as failure
'''

class MyBaseFailure(BaseException):
    pass

'''
error type exceptions
this exceptions will mark test as error
'''

class MyBaseError(Exception):
    pass

class FileFormatError(MyBaseError):
    pass

class ParamsError(MyBaseError):
    pass

class NotFoundError(MyBaseError):
    pass

class FileNotFoundError(NotFoundError):
    pass

class FunctionNotFoundError(NotFoundError):
    pass