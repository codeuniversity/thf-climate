from src.gee.auth import authenticate


def test_gee_authenticate_basic():
    assert authenticate() is None
