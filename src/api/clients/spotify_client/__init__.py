from .client import SpotifyClient
import src.api.clients.logging_client as logging_client
import src.api.clients.spotify_auth_client as spotify_auth_client
import src.api.config as config

spotify_client = SpotifyClient(spotify_auth_client, logging_client.logging_client, config.config)