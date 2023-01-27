import os

class EnvironmentVariableProxy():
    def get_environment_variable(self, key: str, default=None) -> str:
        return os.getenv(key, default=default)
