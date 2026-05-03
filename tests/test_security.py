from app.core.security import hash_password, verify_password


def test_password_hash():
    password = "Test1234"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True

def test_password_verify_fail():
    password = "Test1234"
    wrong_password = "Wrong1234"

    hashed = hash_password(password)

    assert verify_password(wrong_password, hashed) is False