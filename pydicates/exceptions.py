

class Error(Exception):
    pass


class UnknownOperation(Error):

    def __init__(self, operation: str):
        super().__init__(f'Unknown operation "{operation}"')
