from app.auth import hash_password, verify_password

def test_password_hash_round_trip() -> None:
    password = "test-only-password"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong-password", hashed)
