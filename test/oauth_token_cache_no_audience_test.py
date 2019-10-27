"""Test OAuthTokenCache.token() behaviour when not audience is given."""
import pytest


def test_no_audience(oauth_token_cache_instance):
    with pytest.raises(ValueError, match="audience is required"):
        oauth_token_cache_instance.token(audience=None)
