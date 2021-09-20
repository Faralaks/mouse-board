class Error(Exception):
    pass

class UnknownError(Error):
    pass
class NoProcessorError(Error):
    pass

class FileNotExistError(Error):
    pass
