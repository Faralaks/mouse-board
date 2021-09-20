class Error(Exception):
    pass

class UnknownError(Error):
    pass
class NoProcessorError(Error):
    pass

class FileNotExistError(Error):
    pass

class BadButtonError(Error):
    pass

class ValLT0Error(Error):
    pass

class BadKeyError(Error):
    pass

class BadConfidenceError(Error):
    pass

