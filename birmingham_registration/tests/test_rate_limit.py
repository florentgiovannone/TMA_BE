from birmingham_registration.rate_limit import MemoryRateLimiter


def test_registration_limits_are_five_per_email_and_thirty_per_ip():
    now = [0.0]
    limiter = MemoryRateLimiter(clock=lambda: now[0])
    for _ in range(5):
        assert limiter.allow_registration("ada@example.com", "10.0.0.1") is True
    assert limiter.allow_registration("ada@example.com", "10.0.0.2") is False
    for index in range(30):
        assert limiter.allow_registration(f"person{index}@example.com", "10.0.0.9") is True
    assert limiter.allow_registration("fresh@example.com", "10.0.0.9") is False
    now[0] += 3601
    assert limiter.allow_registration("ada@example.com", "10.0.0.1") is True


def test_a_denied_sixth_email_request_does_not_extend_the_hourly_lockout():
    now = [0.0]
    limiter = MemoryRateLimiter(clock=lambda: now[0])
    for _ in range(5):
        assert limiter.allow_registration("ada@example.com", "10.0.0.1") is True
    assert limiter.allow_registration("ada@example.com", "10.0.0.2") is False
    now[0] += 3601
    assert limiter.allow_registration("ada@example.com", "10.0.0.1") is True


def test_five_failed_logins_pause_that_ip_for_fifteen_minutes():
    now = [0.0]
    limiter = MemoryRateLimiter(clock=lambda: now[0])
    for _ in range(4):
        assert limiter.allow_login("10.0.0.1") is True
        limiter.record_login_failure("10.0.0.1")
    assert limiter.allow_login("10.0.0.1") is True
    limiter.record_login_failure("10.0.0.1")
    assert limiter.allow_login("10.0.0.1") is False
    assert limiter.allow_login("10.0.0.2") is True
    now[0] += 15 * 60
    assert limiter.allow_login("10.0.0.1") is True
    limiter.record_login_success("10.0.0.1")
    assert limiter.allow_login("10.0.0.1") is True
