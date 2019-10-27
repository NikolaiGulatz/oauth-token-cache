"""
Test OAuthTokenCache.token() behaviour when forcing a refresh.
"""
import pytest
from unittest import mock

from oauth_token_cache import TokenClient


@mock.patch.object(TokenClient, "cached_token")
@mock.patch.object(TokenClient, "fresh_token")
def test_refresh(
    mock_fresh_token,
    mock_cached_token,
    oauth_token_cache_instance,
    audience,
    make_token,
):
    """When calling token with refresh, it should skip the cache and refresh the token."""
    new_token = make_token(access_token="new_token")

    mock_fresh_token.return_value = new_token
    oauth_token_cache_instance.tokens[audience] = make_token(access_token="old_token")

    assert (
        oauth_token_cache_instance.token(audience=audience, refresh=True) == new_token
    )

    mock_fresh_token.assert_called_once()
    mock_cached_token.assert_not_called()
