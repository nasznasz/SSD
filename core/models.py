from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# ============================================================
#  Developer 2 :  RBAC  (Role-Based Access Control)
# ------------------------------------------------------------
#  Every User gets exactly one Profile that stores their role.
#  Roles: 'admin'  -> full access (view audit log, all users)
#         'user'   -> normal user (own tasks only)
#  OWASP ASVS V4 / A5 - Access Control
# ============================================================
class Profile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'Normal User'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    @property
    def is_admin(self):
        return self.role == 'admin'


# Automatically create / keep a Profile for every User.
@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        # Django superusers are treated as admins by default.
        role = 'admin' if instance.is_superuser else 'user'
        Profile.objects.create(user=instance, role=role)
    else:
        # make sure a profile always exists (e.g. for pre-existing users)
        Profile.objects.get_or_create(user=instance)


# ============================================================
#  Developer 2 :  AUDIT LOG  (Logging & Monitoring)
# ------------------------------------------------------------
#  Records login attempts (success/fail), logouts and important
#  admin actions.  No sensitive data (no passwords) is stored.
#  OWASP ASVS V7 - Logging & Monitoring
# ============================================================
class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('login_success', 'Login Success'),
        ('login_failed', 'Login Failed'),
        ('logout', 'Logout'),
        ('register', 'Registration'),
        ('access_denied', 'Access Denied'),
    ]

    # username is stored as text so we still log FAILED logins for
    # usernames that may not exist in the system.
    username = models.CharField(max_length=150)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True, default='')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"[{self.timestamp:%Y-%m-%d %H:%M:%S}] {self.username} - {self.get_action_display()}"


# ============================================================
#  Developer 1 :  Secure CRUD module  (unchanged)
# ============================================================
class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
