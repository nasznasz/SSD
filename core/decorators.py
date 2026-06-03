"""
Developer 2 : Access Control helpers (RBAC enforcement)
OWASP ASVS V4 / A5 - Access Control

Use @admin_required on any view that only admins may reach.
Denied attempts are written to the AuditLog so we can monitor them.
"""
from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import AuditLog


def _client_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def admin_required(view_func):
    """Allow only users whose Profile role is 'admin'."""
    @wraps(view_func)
    @login_required
    def _wrapped(request, *args, **kwargs):
        profile = getattr(request.user, 'profile', None)
        if profile is None or not profile.is_admin:
            # Log the denied access attempt (no sensitive data stored)
            AuditLog.objects.create(
                username=request.user.username,
                action='access_denied',
                ip_address=_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:255],
            )
            # 403 -> Developer 1's custom error page is shown
            raise PermissionDenied("You do not have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped
