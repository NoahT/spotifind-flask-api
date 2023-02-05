""" Initialization for spotify_auth_client package. """
from src.api.config import config
from .client import SpotifyAuthClient

spotify_auth_client = SpotifyAuthClient(config)
