import src.api.clients.logging_client as logging_client
import src.api.config as config
from .client import SpotifyAuthClient

spotify_auth_client = SpotifyAuthClient(logging_client.logging_client, config.config)