from birmingham_registration.mailer import confirmation_html, confirmation_subject, confirmation_text


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
    assert 'src="cid:brand-mark"' in page
    assert "Birmingham Conference" in page
    assert "Confirm my interest" in page
    assert 'href="https://interest.example.com/confirm?token=abc"' in page
    assert 'bgcolor="#0e2347"' in page
    assert 'bgcolor="#f4f0e8"' in page
    assert 'bgcolor="#fbf9f6"' in page
    assert "#b08958" in page
    assert "color-scheme" in page
    assert "Ada" not in page
