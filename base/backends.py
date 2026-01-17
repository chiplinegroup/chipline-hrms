import os
import logging
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

# =====================================================
# LOGGER (⚠️ REQUIRED BY OTHER APPS)
# =====================================================
logger = logging.getLogger(__name__)


# =====================================================
# BREVO (Sendinblue) API Email Backend — NO SMTP
# =====================================================

class BrevoEmailBackend(BaseEmailBackend):
    """
    Sends email using Brevo Transactional Email API.
    NO SMTP. Safe for Render.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        api_key = getattr(settings, "BREVO_API_KEY", None)
        if not api_key:
            logger.warning("BREVO_API_KEY not set. Email disabled.")
            self.enabled = False
            return

        self.enabled = True

        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key["api-key"] = api_key
        api_client = sib_api_v3_sdk.ApiClient(configuration)
        self.api_instance = sib_api_v3_sdk.TransactionalEmailsApi(api_client)

        self.from_email = getattr(
            settings,
            "DEFAULT_FROM_EMAIL",
            "no-reply@example.com",
        )

    def send_messages(self, email_messages):
        if not self.enabled:
            return 0

        sent = 0

        for message in email_messages:
            try:
                email = sib_api_v3_sdk.SendSmtpEmail(
                    to=[{"email": addr} for addr in message.to],
                    subject=message.subject,
                    html_content=message.body,
                    sender={
                        "email": self.from_email,
                        "name": "HRMS",
                    },
                )

                self.api_instance.send_transac_email(email)
                sent += 1

            except ApiException as e:
                logger.error("Brevo email error: %s", e)

        return sent


# =====================================================
# COMPATIBILITY BACKEND (⚠️ DO NOT REMOVE)
# =====================================================
# Existing Horilla code imports this by name
# =====================================================

class ConfiguredEmailBackend(BrevoEmailBackend):
    """
    Backward-compatible alias.
    """
    pass

