from apps.accounts.services.utils import send_template_email
from django.conf import settings
from apps.accounts.models import User

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