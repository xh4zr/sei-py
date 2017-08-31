class SeiException(Exception):
    def __init__(self, message, errors):
        super(SeiException, self).__init__(message)
        self.errors = errors
