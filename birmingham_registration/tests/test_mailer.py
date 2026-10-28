import pytest
import smtplib

from birmingham_registration.mailer import (
    MailgunMailer,
    confirmation_html,
    confirmation_subject,
    confirmation_text,
    contact_service_html,
    contact_service_subject,
    contact_service_text,
    contact_thank_you_html,
    contact_thank_you_subject,
    contact_thank_you_text,
    mailgun_smtp_host,
    mailgun_smtp_port,
)


def test_confirmation_email_names_the_artwork_and_the_five_minute_limit():
    text = confirmation_text("The Star of Bethlehem", "https://interest.example.com/confirm?token=abc")
    assert "The Star of Bethlehem" in text
    assert "https://interest.example.com/confirm?token=abc" in text
    assert "5 minutes" in text
    assert "If you did not ask for this email, you can ignore it." in text
    assert "Ada" not in text
    assert "@" not in text.split("token=abc")[0]


def test_confirmation_email_uses_the_birmingham_layout():
    url = "https://interest.example.com/confirm?token=abc"
    page = confirmation_html("The Star of Bethlehem", url)
    assert confirmation_subject("The Star of Bethlehem") == "Confirm your interest in The Star of Bethlehem"
    assert "TAKE" in page
    assert "ME" in page
    assert "AROUND" in page
    assert 'src="cid:brand-mark.png"' in page
    assert "Museum Association Conference" in page
    assert "Birmingham Conference" not in page
    assert "Confirm my interest" in page
    assert 'href="https://interest.example.com/confirm?token=abc"' in page
    assert f">{url}</a>" not in page
    assert 'bgcolor="#0e2347"' in page
    assert 'bgcolor="#f4f0e8"' in page
    assert 'bgcolor="#fbf9f6"' in page
    assert "#b08958" in page
    assert "color-scheme" in page
    assert "mix-blend-mode" not in page
    assert "Ada" not in page


def test_mailgun_sends_the_confirmation_over_smtp(monkeypatch):
    captured = {}

    class FakeSMTP:
        def __init__(self, host, port, timeout):
            captured["host"] = host
            captured["port"] = port
            captured["timeout"] = timeout

        def ehlo(self):
            return (250, b"ok")

        def starttls(self):
            captured["starttls"] = True

        def login(self, username, password):
            captured["username"] = username
            captured["password"] = password

        def send_message(self, message):
            captured["message"] = message

        def quit(self):
            captured["quit"] = True

    monkeypatch.setattr("birmingham_registration.mailer.smtplib.SMTP", FakeSMTP)
    MailgunMailer(
        "smtp.eu.mailgun.org",
        587,
        "confirmation@mg.example.com",
        "secret",
        "Interest <confirmation@mg.example.com>",
    ).send_confirmation(
        "ada@example.com",
        "The Star of Bethlehem",
        "https://interest.example.com/confirm?token=abc",
    )
    assert captured["host"] == "smtp.eu.mailgun.org"
    assert captured["port"] == 587
    assert captured["timeout"] == 20
    assert captured["starttls"] is True
    assert captured["username"] == "confirmation@mg.example.com"
    assert captured["password"] == "secret"
    assert captured["quit"] is True
    message = captured["message"]
    bodies = [
        part.get_content()
        for part in message.walk()
        if part.get_content_maintype() == "text"
    ]
    body = "\n".join(bodies)
    assert message["To"] == "ada@example.com"
    assert message["Subject"] == "Confirm your interest in The Star of Bethlehem"
    assert "cid:brand-mark.png" in body
    assert "https://interest.example.com/confirm?token=abc" in body


def test_mailgun_raises_when_smtp_rejects_the_login(monkeypatch):
    class FakeSMTP:
        def __init__(self, host, port, timeout):
            pass

        def ehlo(self):
            return (250, b"ok")

        def starttls(self):
            return (220, b"ready")

        def login(self, username, password):
            raise smtplib.SMTPAuthenticationError(535, b"auth failed")

        def quit(self):
            pass

    monkeypatch.setattr("birmingham_registration.mailer.smtplib.SMTP", FakeSMTP)
    with pytest.raises(smtplib.SMTPAuthenticationError):
        MailgunMailer(
            "smtp.eu.mailgun.org",
            587,
            "confirmation@mg.example.com",
            "secret",
            "Interest <confirmation@mg.example.com>",
        ).send_confirmation("ada@example.com", "The Golden Boys", "https://interest.example.com/confirm?token=abc")


def test_contact_thank_you_email_greets_the_user_in_text_and_html():
    assert contact_thank_you_subject() == "Thank you for contacting Take Me Around"
    text = contact_thank_you_text("Ada <Lovelace>")
    assert "Ada <Lovelace>" in text
    assert "Thank you for getting in touch with Take Me Around." in text
    assert "at the Museum Association Conference" not in text
    page = contact_thank_you_html("Ada <Lovelace>")
    assert "Ada &lt;Lovelace&gt;" in page
    assert "<Lovelace>" not in page
    assert 'src="cid:brand-mark.png"' in page
    assert "Thank you for getting in touch with Take Me Around." in page
    assert "at the Museum Association Conference" not in page
    assert "Museum Association Conference" in page
    assert "Birmingham Conference" not in page


def test_contact_service_email_includes_user_details_and_escapes_html():
    values = {
        "name": "Ada Lovelace",
        "email": "ada@example.com",
        "organisation": "Analytical <Engines>",
        "message": "Line one\nLine <two>",
    }
    assert contact_service_subject("Ada\r\nLovelace") == "Museum Association Conference enquiry from Ada Lovelace"
    text = contact_service_text(values)
    assert "Museum Association Conference" in text
    assert "Name: Ada Lovelace" in text
    assert "Email: ada@example.com" in text
    assert "Organisation: Analytical <Engines>" in text
    assert "Line one\nLine <two>" in text
    page = contact_service_html(values)
    assert "Museum Association Conference" in page
    assert "Ada Lovelace" in page
    assert "ada@example.com" in page
    assert "Analytical &lt;Engines&gt;" in page
    assert "Line one<br />Line &lt;two&gt;" in page
    assert "<two>" not in page
    empty_org = {**values, "organisation": ""}
    assert "Organisation: —" in contact_service_text(empty_org)
    assert "<strong>Organisation:</strong> —" in contact_service_html(empty_org)


def test_mailgun_sends_contact_thank_you_and_service_emails_with_reply_to(monkeypatch):
    sent_messages = []

    class FakeSMTP:
        def __init__(self, host, port, timeout):
            pass

        def ehlo(self):
            return (250, b"ok")

        def starttls(self):
            return (220, b"ready")

        def login(self, username, password):
            pass

        def send_message(self, message):
            sent_messages.append(message)

        def quit(self):
            pass

    monkeypatch.setattr("birmingham_registration.mailer.smtplib.SMTP", FakeSMTP)
    mailer = MailgunMailer(
        "smtp.eu.mailgun.org",
        587,
        "confirmation@mg.example.com",
        "secret",
        "Take Me Around <confirmation@mg.example.com>",
    )
    values = {
        "name": "Ada Lovelace",
        "email": "ada@example.com",
        "organisation": "",
        "message": "We host a sculpture trail.",
    }
    mailer.send_contact_service_email("info@takemearound.com", values)
    mailer.send_contact_thank_you("ada@example.com", "Ada Lovelace")

    assert len(sent_messages) == 2
    service_msg, thank_you_msg = sent_messages
    assert service_msg["To"] == "info@takemearound.com"
    assert service_msg["Reply-To"] == "ada@example.com"
    assert service_msg["Subject"] == "Museum Association Conference enquiry from Ada Lovelace"
    assert thank_you_msg["To"] == "ada@example.com"
    assert thank_you_msg["Subject"] == "Thank you for contacting Take Me Around"


def test_mailgun_smtp_host_and_port_are_limited():
    assert mailgun_smtp_host(" SMTP.EU.MAILGUN.ORG ") == "smtp.eu.mailgun.org"
    assert mailgun_smtp_port("587") == 587
    with pytest.raises(RuntimeError):
        mailgun_smtp_host("smtp.example.com")
    with pytest.raises(RuntimeError):
        mailgun_smtp_port("25")
