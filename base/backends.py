import logging
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

# --------------------------------------------------
# Logger (used by other apps like attendance, base)
# --------------------------------------------------
logger = logging.getLogger(__name__)


# --------------------------------------------------
# Brevo Email Backend (API only – NO SMTP)
# Works for:
# - Password reset emails
# - Document request emails
# - All Django system emails
# --------------------------------------------------
class BrevoEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        api_key = getattr(settings, "BREVO_API_KEY", None)

        if not api_key:
            logger.error("BREVO_API_KEY is missing")
            return 0

        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key["api-key"] = api_key
        api_client = sib_api_v3_sdk.ApiClient(configuration)
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(api_client)

        sent_count = 0

        for message in email_messages:
            try:
                # Convert plain text → HTML (required by Brevo)
                html_content = message.body.replace("\n", "<br>")

                email = sib_api_v3_sdk.SendSmtpEmail(
                    to=[{"email": addr} for addr in message.to],
                    subject=message.subject,
                    html_content=html_content,
                    sender={
                        "email": settings.DEFAULT_FROM_EMAIL,
                        "name": getattr(settings, "EMAIL_FROM_NAME", "Chipline HRMS"),
                    },
                )

                api_instance.send_transac_email(email)
                sent_count += 1

            except ApiException as e:
                logger.error(f"Brevo email API error: {e}")
            except Exception as e:
                logger.error(f"Unexpected email error: {e}")

        return sent_count


# --------------------------------------------------
# Backward compatibility
# (Other modules import this name)
# --------------------------------------------------
ConfiguredEmailBackend = BrevoEmailBackend

