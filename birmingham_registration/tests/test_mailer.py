from birmingham_registration.mailer import confirmation_text


def test_confirmation_email_names_the_artwork_and_the_five_minute_limit():
    text = confirmation_text("The Star of Bethlehem", "https://interest.example.com/confirm?token=abc")
    assert "The Star of Bethlehem" in text
    assert "https://interest.example.com/confirm?token=abc" in text
    assert "5 minutes" in text
    assert "Ada" not in text
    assert "@" not in text.split("token=abc")[0]
