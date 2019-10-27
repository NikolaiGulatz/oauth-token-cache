"""Token"""
import time


class Token:
    """An OAuth 2.0 token which is aware of its expiry.

    Args:
        access_token (str): The OAuth 2.0 access token
        expires_in (int): Number of seconds to expiration
        token_type (str): Type of the access token
        audience (str): Audience for which the access token has been issued
        expires_at (:obj:`int`, optional): UNIX timestamp of expiry

    Attributes:
        expires_in (int): Original number of seconds to expiration
        expires_at (int): UNIX timestamp of expiry
        access_token (str): The OAuth 2.0 access token
        token_type (str): The token type
        audience (str): Audience for which the access token has been issued
    """

    def __init__(
        self,
        access_token=None,
        expires_in=None,
        expires_at=None,
        token_type=None,
        audience=None,
    ):
        self.access_token = access_token
        self.expires_in = expires_in
        self.expires_at = expires_at
        self.token_type = token_type
        self.audience = audience

    @classmethod
    def from_auth_provider(
        cls, access_token=None, expires_in=None, token_type=None, audience=None
    ):
        """Initialize a fresh token from the auth provider.

        Args:
            access_token (str)
            expires_in (int)
            token_type (str)
            audience (str)

        Returns:
            Token: An instance of Token
        """
        expires_at = int(time.time()) + expires_in

        return cls(
            access_token=access_token,
            expires_in=expires_in,
            expires_at=expires_at,
            token_type=token_type,
            audience=audience,
        )

    @classmethod
    def from_cache(cls, cached_token):
        """Initialize a token from cache.

        Args:
            cached_token (dict)

        Returns:
            Token: An instance of Token
        """
        return cls(
            access_token=cached_token["access_token"],
            expires_in=int(cached_token["expires_in"]),
            expires_at=int(cached_token["expires_at"]),
            token_type=cached_token["token_type"],
            audience=cached_token["audience"],
        )

    def __repr__(self):
        return (
            f"<Token access_token='{self.access_token}' expires_in='{self.expires_in}' expires_at='{self.expires_at}'"
            f" token_type='{self.token_type}' audience='{self.audience}' expired='{self.expired}'>"
        )

    def __eq__(self, obj):
        return isinstance(obj, Token) and obj.asdict() == self.asdict()

    @property
    def expired(self):
        """Whether or not the token has expired.

        Returns:
            bool: Whether or not the token has expired.
        """
        return int(time.time()) > self.expires_at

    def asdict(self):
        """Serialize token into a dict.

        Returns:
            dict: The serialized token
        """
        return {
            "access_token": self.access_token,
            "audience": self.audience,
            "token_type": self.token_type,
            "expires_in": self.expires_in,
            "expires_at": self.expires_at,
        }
