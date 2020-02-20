import os
import re
import time
import pytest

import redis

from oauth_token_cache import OAuthTokenCache, TokenClient, Token


def scrub_access_token():
    def before_record_response(response):
        response["body"]["string"] = bytes(
            re.sub(
                r'"([a-zA-Z0-9_\-\.=]{32,})"',
                '"secret"',
                response["body"]["string"].decode("utf-8"),
            ),
            "utf-8",
        )

        return response

    return before_record_response


@pytest.fixture(scope="module")
def vcr(vcr):
    vcr.filter_post_data_parameters = [
        ("client_id", "secret"),
        ("client_secret", "secret"),
    ]
    vcr.match_on = ["method", "scheme", "port", "path"]
    vcr.before_record_response = scrub_access_token()
    return vcr


@pytest.fixture
def oauth_token():
    return "AYjcyMzY3ZDhiNmJkNTY"


@pytest.fixture
def redis_client():
    return redis.Redis(**OAuthTokenCache.REDIS_DEFAULTS)


@pytest.fixture
def client_id():
    return os.environ.get("CLIENT_ID") or "XXX"


@pytest.fixture
def client_secret():
    return os.environ.get("CLIENT_SECRET") or "XXX"


@pytest.fixture
def token_url():
    return os.environ.get("TOKEN_URL") or "https://example.com/oauth/token"


@pytest.fixture
def audience():
    return os.environ.get("AUDIENCE") or "test"


@pytest.fixture
def oauth_token_cache_instance(client_id, client_secret, token_url):
    return OAuthTokenCache(
        client_id=client_id, client_secret=client_secret, token_url=token_url
    )


@pytest.fixture
def make_token_client(redis_client, client_id, client_secret, token_url, audience):
    TOKEN_CLIENT_DEFAULTS = {
        "client_id": client_id,
        "client_secret": client_secret,
        "token_url": token_url,
        "redis_client": redis_client,
        "audience": audience,
    }

    redis_client.flushall()

    def _make_token_client(*args, **kwargs):
        return TokenClient(**{**TOKEN_CLIENT_DEFAULTS, **kwargs})

    return _make_token_client


@pytest.fixture
def make_token():
    TOKEN_DEFAULTS = {
        "access_token": "access_token",
        "expires_in": 3600,
        "expires_at": int(time.time()) + 3600,
        "token_type": "Bearer",
        "audience": "test",
    }

    def _make_token(*args, **kwargs):
        return Token(**{**TOKEN_DEFAULTS, **kwargs})

    return _make_token
