# oauth-token-cache

[![Build Status](https://travis-ci.org/NikolaiGulatz/oauth-token-cache.svg?branch=master)](https://travis-ci.org/NikolaiGulatz/oauth-token-cache) [![codecov](https://codecov.io/gh/NikolaiGulatz/oauth-token-cache/branch/master/graph/badge.svg)](https://codecov.io/gh/NikolaiGulatz/oauth-token-cache)

Easily obtain and cache OAuth 2.0 JWT tokens from Auth0.

When using external auth providers for obtaining OAuth 2.0 machine-to-machine tokens you may want to share one access
token across several instances (e.g. processes, threads, containers, pods ...) of your application in order to avoid
having to issue new tokens too often.

oauth-token-cache makes it easy to obtain, refresh and cache OAuth 2.0 tokens. Obtained tokens are stored both in
memory and in Redis with a TTL which corresponds to the time to expire of your token.

## Quickstart

```python
from oauth_token_cache import OAuthTokenCache

token_provider = OAuthTokenCache(
    client_id="XXX",
    client_secret="XXX",
    token_url="https://example.com/oauth/token"
)

# The token will be cached in Redis. A fresh token will automatically be
# fetched when calling `token` the next time in case the old token has
# expired.
my_token = token_provider.token(audience="test")

my_token.access_token
>> eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlFrVkJOemN6TjBNeFJr...

my_token.audience
>> test

my_token.token_type
>> Bearer

my_token.expires_at
>> 1572169916

my_token.expired
>> False
```

## Configuring Redis

The `redis_options` argument will be passed on to the redis client. See the [documentation of the redis package](https://pypi.org/project/redis/) on how to configure the client.

```python
OAuthTokenCache(
    client_id="XXX",
    client_secret="XXX",
    token_url="https://example.com/oauth/token",
    redis_options={
        "host": "example.com",
        "port": 1234,
    }
)
```

### Using your own Redis client

You can pass your own Redis client at which `redis_options` will be ignored.

```python
redis_client = redis.Redis()

OAuthTokenCache(
    client_id="XXX",
    client_secret="XXX",
    token_url="https://example.com/oauth/token",
    redis_client=redis_client,
)
```
