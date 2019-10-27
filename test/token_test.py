import time
import pytest

from freezegun import freeze_time
from oauth_token_cache import Token


@pytest.fixture
def expires_in():
    return 3600


@pytest.fixture
def token(expires_in):
    return Token(
        access_token="XXX", expires_in=expires_in, token_type="Bearer", audience="test"
    )


def test_expires_at(token, expires_in):
    assert token.expires_at == int(time.time()) + expires_in


def test_non_expired_token(token):
    assert token.expired == False


def test_expired_token(token, expires_in):
    with freeze_time("2019-01-01"):
        expired_token = Token(
            access_token="XXX",
            expires_in=expires_in,
            token_type="Bearer",
            audience="test",
        )

    assert expired_token.expired == True


def test_asdict(token, expires_in):
    assert isinstance(token.asdict(), dict)
