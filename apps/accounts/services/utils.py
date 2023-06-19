from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail

def send_template_email(template, email, subject, **context):
    context["instagram_url"] = settings.SOCIAL_MEDIA_INSTAGRAM_URL
    context["facebook_url"] = settings.SOCIAL_MEDIA_FACEBOOK_URL
    context["linkedin_url"] = settings.SOCIAL_MEDIA_LINKEDIN_URL
    context["twitter_url"] = settings.SOCIAL_MEDIA_TWITTER_URL
    
    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)

    send_mail(
        subject,
        plain_message,
        "ProteinTech <{}>".format(settings.EMAIL_HOST_USER),
        [email],
        html_message=html_message,
    )