import logging
import re


class RedactTokenFilter(logging.Filter):
    pattern = re.compile(r"token=[^&\s\"']+")

    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = self._redact(record.msg)
        if isinstance(record.args, tuple):
            record.args = tuple(self._redact(arg) for arg in record.args)
        elif isinstance(record.args, dict):
            record.args = {key: self._redact(value) for key, value in record.args.items()}
        return True

    def _redact(self, value):
        if isinstance(value, str):
            return self.pattern.sub("token=redacted", value)
        return value
