from django.contrib import admin
from .models import AuditLog, LoginAttempt


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'model_name', 'object_repr', 'ip_address', 'timestamp')
    list_filter = ('action', 'model_name')
    search_fields = ('user__username', 'model_name', 'object_repr', 'ip_address')
    readonly_fields = ('user', 'action', 'model_name', 'object_id', 'object_repr', 'changes', 'ip_address', 'user_agent', 'timestamp')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ('username_attempted', 'user', 'success', 'ip_address', 'timestamp')
    list_filter = ('success',)
    search_fields = ('username_attempted', 'ip_address')
    readonly_fields = ('username_attempted', 'user', 'ip_address', 'user_agent', 'success', 'timestamp')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False