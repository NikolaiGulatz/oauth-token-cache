import time
import pytest

from freezegun import freeze_time
from oauth_token_cache import Token


@pytest.fixture
def expires_in():
    return 3600

def test_from_auth_provider(expires_in):
    token = Token.from_auth_provider(
        access_token="XXX",
        expires_in=expires_in,
        token_type="Bearer",
        audience="test",
    )

    assert token.expires_at == int(time.time()) + expires_in
    assert token.expired == False

    with freeze_time("2019-01-01"):
        expired_token = Token.from_auth_provider(
            access_token="XXX",
            expires_in=expires_in,
            token_type="Bearer",
            audience="test",
        )

    assert expired_token.expired == True

def test_from_cache(expires_in):
    token = Token.from_cache(
        {
            "access_token": "XXX",
            "expires_in": 1,
            "expires_at": 1,
            "token_type": "Bearer",
            "audience": "test",
        }
    )

    assert token.expired == True

def test_active_token(make_token, expires_in):
    token = make_token(expires_in=expires_in)

    assert token.expires_at == int(time.time()) + expires_in
    assert token.expired == False

def test_expired_token(make_token, expires_in):
    with freeze_time("2019-01-01"):
        expired_token = make_token(
            access_token="XXX",
            expires_in=expires_in,
            expires_at=int(time.time()),
            token_type="Bearer",
            audience="test",
        )

    assert expired_token.expired == True


def test_asdict(make_token, expires_in):
    dict_token = make_token().asdict()
    required_keys = ["access_token", "audience", "token_type", "expires_in", "expires_at"]

    assert isinstance(dict_token, dict)
    assert list(dict_token.keys()).sort() == required_keys.sort()
