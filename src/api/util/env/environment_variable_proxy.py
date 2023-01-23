import os

class EnvironmentVariableProxy():
    def get_environment_variable(self, key: str) -> str:
        return os.environ[key]