"""Test OAuthTokenCache.token() caching behaviour."""

import pytest
from unittest import mock

from oauth_token_cache import TokenClient


@mock.patch.object(TokenClient, "cached_token")
@mock.patch.object(TokenClient, "fresh_token")
def test_existing_local_token(
    mock_fresh_token,
    mock_cached_token,
    oauth_token_cache_instance,
    audience,
    make_token,
):
    """Valid token in the local cache. Do not check the redis cache and do not issue a fresh token."""
    token = make_token()

    mock_fresh_token.return_value = token
    oauth_token_cache_instance.tokens[audience] = token

    assert oauth_token_cache_instance.token(audience=audience) == token

    mock_fresh_token.assert_not_called()
    mock_cached_token.assert_not_called()


@mock.patch.object(TokenClient, "cached_token")
@mock.patch.object(TokenClient, "fresh_token")
def test_expired_local_token(
    mock_fresh_token,
    mock_cached_token,
    oauth_token_cache_instance,
    audience,
    make_token,
):
    """Expired token in the local cache, no token in the redis cache. Issue a new token after checking both."""
    token = make_token()
    expired_token = make_token(expires_at=-1)

    mock_cached_token.return_value = None
    mock_fresh_token.return_value = token
    oauth_token_cache_instance.tokens[audience] = expired_token

    assert oauth_token_cache_instance.token(audience=audience) == token

    mock_fresh_token.assert_called_once()
    mock_cached_token.assert_called_once()


@mock.patch.object(TokenClient, "cached_token")
@mock.patch.object(TokenClient, "fresh_token")
def test_redis_cache_hit(
    mock_fresh_token,
    mock_cached_token,
    oauth_token_cache_instance,
    audience,
    make_token,
):
    """No token in the local cache, token cached in the redis cache. Return token from redis cache without
    issueing a fresh token.
    """
    token = make_token()

    mock_cached_token.return_value = token

    assert oauth_token_cache_instance.token(audience=audience) == token

    mock_fresh_token.assert_not_called()
    mock_cached_token.assert_called_once()


@mock.patch.object(TokenClient, "cached_token")
@mock.patch.object(TokenClient, "fresh_token")
def test_multiple_redis_cache_hits(
    mock_fresh_token,
    mock_cached_token,
    oauth_token_cache_instance,
    audience,
    make_token,
):
    """No token in the local cache, token cached in the redis cache. Return token from redis cache without
    issueing a fresh token, but only check redis cache once.
    """
    token = make_token()

    mock_cached_token.return_value = token

    for i in range(3):
        assert oauth_token_cache_instance.token(audience=audience) == token

    mock_fresh_token.assert_not_called()
    mock_cached_token.assert_called_once()


@mock.patch.object(TokenClient, "cached_token")
@mock.patch.object(TokenClient, "fresh_token")
def test_multiple_redis_cache_misses(
    mock_fresh_token,
    mock_cached_token,
    oauth_token_cache_instance,
    audience,
    make_token,
):
    """No token in the local cache, no token in the redis cache. Issue a new token after checking both."""
    token = make_token()

    mock_fresh_token.return_value = token
    mock_cached_token.return_value = None

    for i in range(3):
        assert oauth_token_cache_instance.token(audience=audience) == token

    mock_fresh_token.assert_called_once()
    mock_cached_token.assert_called_once()


@mock.patch.object(TokenClient, "cached_token")
@mock.patch.object(TokenClient, "fresh_token")
def test_multiple_audiences(
    mock_fresh_token,
    mock_cached_token,
    oauth_token_cache_instance,
    audience,
    make_token,
):
    """No token in local cache, add tokens for two different audiences and check correct caching."""
    first_token = make_token(access_token="first")
    second_token = make_token(access_token="second")

    mock_cached_token.return_value = first_token

    for i in range(3):
        assert oauth_token_cache_instance.token(audience="first") == first_token

    mock_cached_token.return_value = second_token

    for i in range(3):
        assert oauth_token_cache_instance.token(audience="second") == second_token

    mock_cached_token.return_value = None

    assert oauth_token_cache_instance.token(audience="first") == first_token
    assert oauth_token_cache_instance.token(audience="second") == second_token

    mock_fresh_token.assert_not_called()
    assert mock_cached_token.call_count == 2
