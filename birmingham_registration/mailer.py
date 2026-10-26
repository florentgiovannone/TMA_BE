import html
import smtplib
from email.message import EmailMessage
from pathlib import Path

_MARK_PNG = Path(__file__).with_name("static").joinpath("brand-mark.png").read_bytes()


def confirmation_subject(artwork_title: str) -> str:
    return f"Confirm your interest in {artwork_title}"


def confirmation_text(artwork_title: str, confirm_url: str) -> str:
    return (
        f"Confirm your interest in {artwork_title}.\n\n"
        "You asked to register your interest in "
        f"{artwork_title}. Open the link below within 5 minutes.\n\n"
        f"{confirm_url}\n\n"
        "If you did not ask for this email, you can ignore it."
    )


def confirmation_html(artwork_title: str, confirm_url: str) -> str:
    title = html.escape(artwork_title)
    url = html.escape(confirm_url, quote=True)
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta name="color-scheme" content="light only" />
    <meta name="supported-color-schemes" content="light" />
    <style>
      :root {{ color-scheme: light only; supported-color-schemes: light; }}
      u + .body .gmail-blend-screen {{ background:#000; mix-blend-mode:screen; }}
      u + .body .gmail-blend-difference {{ background:#000; mix-blend-mode:difference; }}
    </style>
  </head>
  <body class="body" bgcolor="#f4f0e8" style="margin:0;padding:0;background:#f4f0e8;background-color:#f4f0e8;">
    <div class="gmail-blend-screen">
      <div class="gmail-blend-difference">
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" bgcolor="#f4f0e8" style="background:#f4f0e8;background-color:#f4f0e8;">
          <tr>
            <td align="center" bgcolor="#f4f0e8" style="padding:32px 16px;background:#f4f0e8;background-color:#f4f0e8;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" bgcolor="#fbf9f6" style="max-width:520px;background:#fbf9f6;background-color:#fbf9f6;">
                <tr>
                  <td bgcolor="#0e2347" style="background:#0e2347;background-color:#0e2347;padding:22px 32px;">
                    <table role="presentation" cellpadding="0" cellspacing="0">
                      <tr>
                        <td style="padding-right:12px;vertical-align:middle;">
                          <img src="cid:brand-mark.png" width="28" height="28" alt="" style="display:block;border:0;" />
                        </td>
                        <td style="vertical-align:middle;">
                          <p style="margin:0;font-family:Georgia,serif;font-size:13px;letter-spacing:0.18em;color:#f7f3ea;">TAKE <span style="color:#b08958;">ME</span> AROUND</p>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
                <tr>
                  <td bgcolor="#fbf9f6" style="padding:28px 32px 32px;background:#fbf9f6;background-color:#fbf9f6;border-top:3px solid #b08958;">
                    <p style="margin:0 0 12px;font-family:'Avenir Next',Avenir,Helvetica,sans-serif;font-size:13px;letter-spacing:0.08em;color:#b08958;">Birmingham Conference</p>
                    <h1 style="margin:0 0 16px;font-family:Georgia,serif;font-size:28px;line-height:1.2;font-weight:normal;color:#0e2347;">Confirm your interest</h1>
                    <p style="margin:0 0 24px;font-family:'Avenir Next',Avenir,Helvetica,sans-serif;font-size:16px;line-height:1.5;color:#243044;">You asked to register your interest in {title}. Open the button below within 5 minutes.</p>
                    <table role="presentation" cellpadding="0" cellspacing="0">
                      <tr>
                        <td bgcolor="#0e2347" style="background:#0e2347;background-color:#0e2347;">
                          <a href="{url}" style="display:inline-block;padding:14px 22px;font-family:'Avenir Next',Avenir,Helvetica,sans-serif;font-size:15px;color:#f7f3ea;text-decoration:none;">Confirm my interest</a>
                        </td>
                      </tr>
                    </table>
                    <p style="margin:20px 0 0;font-family:'Avenir Next',Avenir,Helvetica,sans-serif;font-size:13px;line-height:1.5;color:#0e2347;word-break:break-all;"><a href="{url}" style="color:#0e2347;text-decoration:underline;">{url}</a></p>
                    <p style="margin:24px 0 0;font-family:'Avenir Next',Avenir,Helvetica,sans-serif;font-size:13px;line-height:1.5;color:#243044;">If you did not ask for this email, you can ignore it.</p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
        </table>
      </div>
    </div>
  </body>
</html>
"""


_SMTP_HOSTS = {"smtp.mailgun.org", "smtp.eu.mailgun.org"}


def mailgun_smtp_host(value: str) -> str:
    host = value.strip().lower()
    if host not in _SMTP_HOSTS:
        raise RuntimeError("MAILGUN_SMTP_HOST must be smtp.mailgun.org or smtp.eu.mailgun.org")
    return host


def mailgun_smtp_port(value: str) -> int:
    if value.strip() not in {"587", "465"}:
        raise RuntimeError("MAILGUN_SMTP_PORT must be 587 or 465")
    return int(value.strip())


class MailgunMailer:
    def __init__(self, host: str, port: int, username: str, password: str, from_address: str):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._from_address = from_address

    def send_confirmation(self, to_email: str, artwork_title: str, confirm_url: str) -> None:
        message = EmailMessage()
        message["From"] = self._from_address
        message["To"] = to_email
        message["Subject"] = confirmation_subject(artwork_title)
        message.set_content(confirmation_text(artwork_title, confirm_url))
        message.add_alternative(confirmation_html(artwork_title, confirm_url), subtype="html")
        html_part = message.get_payload()[1]
        html_part.add_related(
            _MARK_PNG,
            maintype="image",
            subtype="png",
            cid="<brand-mark.png>",
            filename="brand-mark.png",
            disposition="inline",
        )
        if self._port == 465:
            client = smtplib.SMTP_SSL(self._host, self._port, timeout=20)
        else:
            client = smtplib.SMTP(self._host, self._port, timeout=20)
        try:
            client.ehlo()
            if self._port != 465:
                client.starttls()
                client.ehlo()
            client.login(self._username, self._password)
            client.send_message(message)
        finally:
            client.quit()
