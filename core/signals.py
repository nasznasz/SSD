"""
Developer 2 : Login attempt logging (Audit Log)
OWASP ASVS V7 - Logging & Monitoring

Hooks Django's built-in auth signals so EVERY login success,
failed login and logout is recorded. We never store passwords.
"""
from django.contrib.auth.signals import (
    user_logged_in, user_logged_out, user_login_failed,
)
from django.dispatch import receiver
from .models import AuditLog


def _client_ip(request):
    if request is None:
        return None
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def _ua(request):
    if request is None:
        return ''
    return request.META.get('HTTP_USER_AGENT', '')[:255]


@receiver(user_logged_in)
def log_login_success(sender, request, user, **kwargs):
    AuditLog.objects.create(
        username=user.username, action='login_success',
        ip_address=_client_ip(request), user_agent=_ua(request),
    )


@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):
    AuditLog.objects.create(
        username=user.username if user else 'unknown', action='logout',
        ip_address=_client_ip(request), user_agent=_ua(request),
    )


@receiver(user_login_failed)
def log_login_failed(sender, credentials, request=None, **kwargs):
    # credentials only carries the username, never the password
    AuditLog.objects.create(
        username=credentials.get('username', 'unknown'), action='login_failed',
        ip_address=_client_ip(request), user_agent=_ua(request),
    )
