import os
import pytest
from unittest import mock

from oauth_token_cache import OAuthTokenCache, TokenClient


@pytest.mark.vcr()
def test_all(oauth_token_cache_instance, make_token_client, audience):
    """ Integration test OAuthTokenCache and make sure that the caching mechanism is working."""
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
