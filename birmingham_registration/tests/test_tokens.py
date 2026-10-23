from birmingham_registration.tokens import hash_token, new_token


def test_token_is_url_safe_and_only_the_hash_is_stable():
    token = new_token()
    assert len(token) >= 32
    assert " " not in token and "&" not in token
    assert hash_token(token) == hash_token(token)
    assert hash_token(token) != token
    assert hash_token("other") != hash_token(token)
