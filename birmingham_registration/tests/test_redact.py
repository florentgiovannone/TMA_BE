import logging

from birmingham_registration.redact import RedactTokenFilter

REQUEST_LINE = '127.0.0.1 "GET /confirm?token=abc123&next=1 HTTP/1.1" 200'


def test_filter_redacts_a_confirmation_token_in_an_access_log():
    record = logging.LogRecord(
        name="werkzeug",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg='127.0.0.1 "GET /confirm?token=abc123&next=1 HTTP/1.1" 200',
        args=(),
        exc_info=None,
    )
    assert RedactTokenFilter().filter(record) is True
    assert "abc123" not in record.msg
    assert "token=redacted" in record.msg


def test_redact_token_in_message():
    record = logging.LogRecord(
        name="werkzeug",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg=REQUEST_LINE,
        args=(),
        exc_info=None,
    )
    RedactTokenFilter().filter(record)
    assert "abc123" not in record.msg
    assert "token=redacted" in record.msg


def test_redact_token_in_args_tuple():
    record = logging.LogRecord(
        name="werkzeug",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="%s",
        args=(REQUEST_LINE,),
        exc_info=None,
    )
    RedactTokenFilter().filter(record)
    assert isinstance(record.args, tuple)
    assert len(record.args) == 1
    assert isinstance(record.args[0], str)
    assert "abc123" not in record.args[0]
    assert "token=redacted" in record.args[0]
