import resend


def confirmation_text(artwork_title: str, confirm_url: str) -> str:
    return (
        f"Confirm your interest in {artwork_title}.\n\n"
        f"Open this link within 5 minutes:\n{confirm_url}\n\n"
        "If you did not ask for this email, you can ignore it."
    )


class ResendMailer:
    def __init__(self, api_key: str, from_address: str):
        self._api_key = api_key
        self._from_address = from_address

    def send_confirmation(self, to_email: str, artwork_title: str, confirm_url: str) -> None:
        resend.api_key = self._api_key
        resend.Emails.send(
            {
                "from": self._from_address,
                "to": [to_email],
                "subject": "Confirm your Birmingham Conference interest",
                "text": confirmation_text(artwork_title, confirm_url),
            }
        )
