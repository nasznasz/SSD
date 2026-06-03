from django.contrib import admin
from .models import Task, Profile, AuditLog


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['title', 'owner__username']


# Developer 2 : manage roles + view audit log from Django admin
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']
    search_fields = ['user__username']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'username', 'action', 'ip_address']
    list_filter = ['action']
    search_fields = ['username', 'ip_address']
    readonly_fields = ['username', 'action', 'ip_address', 'user_agent', 'timestamp']

    def has_add_permission(self, request):
        return False  # audit entries are system-generated only
