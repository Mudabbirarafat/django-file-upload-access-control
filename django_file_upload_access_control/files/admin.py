
from django.contrib import admin
from .models import UploadedFile


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ['filename', 'owner', 'created_at', 'encrypted']
    list_filter = ['created_at', 'encrypted', 'owner']
    search_fields = ['filename', 'owner__username']
    readonly_fields = ['id', 'created_at']
    filter_horizontal = ['allowed_users']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(owner=request.user)
        return qs
