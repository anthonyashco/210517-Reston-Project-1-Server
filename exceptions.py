class PermissionDenied(Exception):
    description: str = "User does not have permission to perform that action."

    def __init__(self, message: str):
        self.message = message


class ResourceNotFound(Exception):
    description: str = "This exception indicates a missing resource."

    def __init__(self, message: str):
        self.message = message


class SettingsNotFound(Exception):
    description: str = "settings.yml is missing."

    def __init__(self, message: str):
        self.message = message
