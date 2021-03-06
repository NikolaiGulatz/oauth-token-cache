import os
import pytest

from unittest import mock

from oauth_token_cache import OAuthTokenCache, TokenClient


@pytest.fixture
def with_mocked_token(oauth_token):
    os.environ["OAUTH_TOKEN"] = oauth_token

    yield

    del os.environ["OAUTH_TOKEN"]


def test_mocked_token(
    oauth_token_cache_instance, audience, oauth_token, with_mocked_token
):
    """Integration test OAuthTokenCache when `OAUTH_TOKEN` environment variable is set"""
    with mock.patch.object(
        TokenClient, "fresh_token"
    ) as mock_fresh_token, mock.patch.object(
        TokenClient, "cached_token"
    ) as mock_cached_token:
        token = oauth_token_cache_instance.token(audience=audience)

        assert os.environ.get("OAUTH_TOKEN") is not None
        assert token.access_token == oauth_token

        mock_cached_token.assert_not_called()
        mock_fresh_token.assert_not_called()


@pytest.mark.vcr()
def test_all(oauth_token_cache_instance, make_token_client, audience):
    """Integration test OAuthTokenCache and make sure that the caching mechanism is working."""
    original_fresh_token = TokenClient.fresh_token

    token_client = make_token_client()

    oauth_token_cache_instance.redis_client.flushdb()

    # this mocks the fresh_token method but still calls the original
    with mock.patch.object(TokenClient, "fresh_token") as mock_fresh_token:

        def side_effect():
            return original_fresh_token(token_client)

        mock_fresh_token.side_effect = side_effect

        for i in range(3):
            oauth_token_cache_instance.token(audience=audience)

        assert mock_fresh_token.call_count == 1

    oauth_token_cache_instance.redis_client.flushdb()
