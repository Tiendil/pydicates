

class Error(Exception):
    pass


class UnknownOperation(Error):

    def __init__(self, context, predicate):
        super().__init__(f'Can not determine operation for context {context} and predicate {predicate}')
