"""
  Environment variable proxy module. To aid with unit testing, we adopted a
  proxy strategy for pulling environment variables. This defers access to
  environment variables until after initialization code for unit test suites.
"""
import os


class EnvironmentVariableProxy():

  def get_environment_variable(self, key: str, default=None) -> str:
    return os.getenv(key, default=default)
