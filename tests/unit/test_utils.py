from src.utils import generate_short_code, is_expired
from datetime import datetime, timedelta

def test_generate_short_code():
    code = generate_short_code()
    assert len(code) == 6
    assert code.isalnum()

def test_is_expired():
    future = datetime.now() + timedelta(days=1)
    past = datetime.now() - timedelta(days=1)
    assert is_expired(None) is False
    assert is_expired(future) is False
    assert is_expired(past) is True