import os
import pytest
import requests

from oauth_token_cache import Token


def test_cache_key(make_token_client, redis_client):
    token_client = make_token_client(client_id="XXX", audience="test")

    assert token_client.cache_key == "oauth_token_cache__XXX_test"


def test_mocked_token(make_token_client, oauth_token):
    token_client = make_token_client()

    result = token_client.mocked_token(oauth_token)

    assert isinstance(result, Token)
    assert result.access_token == oauth_token


@pytest.mark.vcr(filter_post_data_parameters=["client_id", "client_secret"])
def test_fresh_token_success(make_token_client, redis_client):
    token_client = make_token_client()

    result = token_client.fresh_token()

    assert isinstance(result, Token)


@pytest.mark.vcr()
def test_fresh_token_unauthorized(make_token_client, redis_client):
    token_client = make_token_client(client_id="XXX")

    with pytest.raises(requests.exceptions.HTTPError):
        token_client.fresh_token()


@pytest.mark.vcr()
def test_fresh_token_wrong_audience(make_token_client, redis_client):
    token_client = make_token_client(audience="foo")

    with pytest.raises(requests.exceptions.HTTPError):
        token_client.fresh_token()


@pytest.mark.vcr()
def test_cached_token(make_token_client, make_token, redis_client):
    token_client = make_token_client()
    token = make_token()

    assert token_client.cached_token() is None

    token_client.cache_token(token)

    assert token_client.cached_token() == token


@pytest.mark.vcr()
def test_cache_token(make_token_client, make_token, redis_client):
    token_client = make_token_client()
    token = make_token()

    assert token_client.cache_token(token) == token
