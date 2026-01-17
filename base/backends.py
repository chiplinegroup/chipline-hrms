from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException


class BrevoEmailBackend(BaseEmailBackend):
    """
    Brevo (Sendinblue) API Email Backend
    Uses HTTP API — NO SMTP (Render safe)
    """

    def send_messages(self, email_messages):
        api_key = getattr(settings, "BREVO_API_KEY", None)

        if not api_key:
            print("❌ BREVO_API_KEY not set")
            return 0

        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key["api-key"] = api_key

        api_client = sib_api_v3_sdk.ApiClient(configuration)
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(api_client)

        sent_count = 0

        for message in email_messages:
            try:
                email = sib_api_v3_sdk.SendSmtpEmail(
                    to=[{"email": addr} for addr in message.to],
                    subject=message.subject,
                    html_content=message.body,
                    sender={
                        "email": getattr(
                            settings,
                            "DEFAULT_FROM_EMAIL",
                            "no-reply@chipline.com",
                        ),
                        "name": "Chipline HRMS",
                    },
                )

                api_instance.send_transac_email(email)
                sent_count += 1

            except ApiException as e:
                print("❌ Brevo email failed:", e)

        return sent_count

