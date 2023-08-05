from apps.accounts.services.utils import send_template_email
from django.conf import settings
from apps.accounts.models import User

import logging
from django.urls import reverse
from django.core.mail import send_mail
from proteintech.settings.celery import app

def send_email(email, content_heading, content_body, detail_area):
    user = User.objects.get(email=email)
    
    send_template_email(
        "default.html",
        user.email,
        "Account Verification",
        **{
            "year": settings.YEAR,
            "content_heading": content_heading,
            "url_placeholders": settings.URL_PLACEHOLDERS,
            "content_body": content_body,
            "detail_area": detail_area,
            "company_address": settings.COMPANY_ADDRESS
        },
    )

@app.task
def send_verification_email(email):
    try:
        user = User.objects.get(email=email)
        send_mail(
            'Verify your QuickPublisher account',
            'Follow this link to verify your account: '
                'http://localhost:8000%s' % reverse('verify', kwargs={'uuid': str(user.verification_uuid)}),
            'from@quickpublisher.dev',
            [user.email],
            fail_silently=False,
        )
    except User.DoesNotExist:
        logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)