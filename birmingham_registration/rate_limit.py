import time
from collections import defaultdict, deque
from collections.abc import Callable


class MemoryRateLimiter:
    def __init__(self, clock: Callable[[], float] | None = None):
        self._clock = clock or time.monotonic
        self._emails: dict[str, deque[float]] = defaultdict(deque)
        self._ips: dict[str, deque[float]] = defaultdict(deque)
        self._contact_emails: dict[str, deque[float]] = defaultdict(deque)
        self._contact_ips: dict[str, deque[float]] = defaultdict(deque)
        self._login_failures: dict[str, int] = {}
        self._login_blocked_until: dict[str, float] = {}

    def allow_registration(self, email: str, ip: str) -> bool:
        now = self._clock()
        email_ok = self._hit(self._emails, email, now, 5)
        ip_ok = self._hit(self._ips, ip, now, 30)
        return email_ok and ip_ok

    def allow_contact(self, email: str, ip: str) -> bool:
        now = self._clock()
        email_ok = self._hit(self._contact_emails, email, now, 5)
        ip_ok = self._hit(self._contact_ips, ip, now, 30)
        return email_ok and ip_ok

    def _hit(self, buckets: dict[str, deque[float]], key: str, now: float, limit: int) -> bool:
        bucket = buckets[key]
        while bucket and now - bucket[0] >= 3600:
            bucket.popleft()
        if not bucket:
            buckets.pop(key, None)
        elif len(bucket) >= limit:
            return False
        bucket = buckets[key]
        bucket.append(now)
        return True

    def allow_login(self, ip: str) -> bool:
        blocked_until = self._login_blocked_until.get(ip)
        now = self._clock()
        if blocked_until is None:
            return True
        if now < blocked_until:
            return False
        self._login_blocked_until.pop(ip, None)
        self._login_failures.pop(ip, None)
        return True

    def record_login_failure(self, ip: str) -> None:
        if not self.allow_login(ip):
            return
        count = self._login_failures.get(ip, 0) + 1
        if count >= 5:
            self._login_blocked_until[ip] = self._clock() + 15 * 60
            self._login_failures[ip] = 0
            return
        self._login_failures[ip] = count

    def record_login_success(self, ip: str) -> None:
        self._login_failures.pop(ip, None)
        self._login_blocked_until.pop(ip, None)
