"""Easily obtain and cache OAuth 2.0 tokens from Auth0

When using external auth providers for obtaining OAuth 2.0 machine-to-machine tokens you may want to share one access
token across several instances (e.g. processes, threads, containers, pods ...) of your application in order to avoid
having to issue new tokens too often.

OAuthTokenCache makes it easy to obtain, refresh and cache OAuth 2.0 tokens. Obtained tokens are stored both in memory
and in Redis with a TTL which corresponds to the time to expire of your token.
"""

import requests
import redis

from .token_client import TokenClient
from .token import Token


class OAuthTokenCache:
    """OAuthTokenCache

    Args:
        client_id (str): The client id
        client_secret (str): The client secret
        token_url (str): The token URL, e.g. https://example.com/oauth/token
        **kwargs: See below.
    """

    REDIS_DEFAULTS = {"decode_responses": True}

    def __init__(self, client_id=None, client_secret=None, token_url=None, **kwargs):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.timeout = kwargs.get("timeout", 5)
        self.redis_options = kwargs.get("redis_options", {})
        self.redis_client = kwargs.get("redis_client", self._default_redis_client())
        self.tokens = {}

    def token(self, audience=None, refresh=False):
        """Obtain a token for the given audience from cache or request a fresh token if
        one of the following conditions is true:

            * The token in the cache is expired
            * There is no token for the given audience in the cache
            * Refresh is forced

        Args:
            audience (str): The audience for which to issue the token
            refresh (:obj:`bool`, optional): Whether to force refresh the token cache,
                defaults to `False`

        Raises:
            ValueError: If audience is missing

        Returns:
            Token: An instance of Token
        """
        if not audience:
            raise ValueError("audience is required")

        token_client = TokenClient(
            client_id=self.client_id,
            client_secret=self.client_secret,
            token_url=self.token_url,
            redis_client=self.redis_client,
            audience=audience,
        )

        if refresh:
            self.tokens[audience] = token_client.fresh_token()
            return self.tokens[audience]

        token = self.tokens.get(audience)

        if not token or token.expired:
            self.tokens[audience] = (
                token_client.cached_token() or token_client.fresh_token()
            )

        return self.tokens[audience]

    def _default_redis_client(self):
        """Create the default redis client.

        Returns:
            redis.Redis: An instance of the redis client
        """
        client = redis.Redis(**{**self.redis_options, **self.REDIS_DEFAULTS})
        client.ping()

        return client
