class NoTableOperatorClassException(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self)
        self.error_info = ErrorInfo
