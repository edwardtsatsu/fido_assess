class ResourceNotCreatedException(Exception):
    def __init__(self, description):
        self.description = description
