class UnknownError(Exception):
    def __init__(self, info="", err=""):
        super().__init__("UnknownError: %s | %s"%(info, err))

class NoProcessorError(Exception):
    def __init__(self, param_name=""):
        super().__init__("No processor for parameter '%s'"%param_name)

class FileNotExistError(Exception):
    def __init__(self, val):
        super().__init__("No such file by path '%s'"%val)

class BadButtonError(Exception):
    def __init__(self, val):
        super().__init__("Btn value must be 'left' or 'right', '%s' was given"%val)

class ValLT0Error(Exception):
    def __init__(self, val, param_name):
        super().__init__("Value '%s' in parameter '%s'  lower then zero"%(val, param_name))

class BadKeyError(Exception):
    def __init__(self, val):
        super().__init__("Key '%s' not available"%val)

class BadConfidenceError(Exception):
    def __init__(self, val):
        super().__init__("Confidence value '%s' not in between 0 and 1"% val)

class TimeLimitReachedError(Exception):
    def __init__(self, val):
        super().__init__("Btn value must be 'left' or 'right', '%s' was given"%val)