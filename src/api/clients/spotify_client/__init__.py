""" Initialization for spotify_client package. """
from .client import SpotifyClient
from src.api.clients import logging_client
from src.api.clients import spotify_auth_client
from src.api import config

spotify_client = SpotifyClient(spotify_auth_client.spotify_auth_client,
                               logging_client.logging_client, config.config)
