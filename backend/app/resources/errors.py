class ObjectNotFoundException(Exception):
    def __init__(self, name: str):
        self.name = name


class ObjectAlreadyExistsException(Exception):
    def __init__(self, name: str):
        self.name = name
