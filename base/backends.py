import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.core.mail.backends.base import BaseEmailBackend


class BrevoEmailBackend(BaseEmailBackend):
    """
    Email backend using Brevo API (NO SMTP)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        api_key = os.getenv("BREVO_API_KEY")
        if not api_key:
            raise Exception("BREVO_API_KEY is missing")

        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key["api-key"] = api_key
        self.client = sib_api_v3_sdk.ApiClient(configuration)
        self.api_instance = sib_api_v3_sdk.TransactionalEmailsApi(self.client)

        self.from_email = os.getenv("EMAIL_FROM", "no-reply@chipline.com")
        self.from_name = os.getenv("EMAIL_FROM_NAME", "Chipline HRMS")

    def send_messages(self, email_messages):
        success_count = 0

        for message in email_messages:
            try:
                email = sib_api_v3_sdk.SendSmtpEmail(
                    to=[{"email": addr} for addr in message.to],
                    subject=message.subject,
                    html_content=message.body,
                    sender={
                        "email": self.from_email,
                        "name": self.from_name,
                    },
                )

                self.api_instance.send_transac_email(email)
                success_count += 1

            except ApiException as e:
                print("Brevo email error:", e)

        return success_count

