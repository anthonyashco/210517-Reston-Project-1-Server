class ResourceNotFound(Exception):
    description: str = "This exception indicates a missing resource."

    def __init__(self, message: str):
        self.message = message
