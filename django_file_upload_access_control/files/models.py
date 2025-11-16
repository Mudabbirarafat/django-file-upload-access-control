
from django.db import models
from django.contrib.auth.models import User
import uuid


class UploadedFile(models.Model):
    """Model for storing encrypted uploaded files with access control."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/')
    filename = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    allowed_users = models.ManyToManyField(User, related_name='shared_files', blank=True)
    encrypted = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Uploaded File'
        verbose_name_plural = 'Uploaded Files'
        indexes = [
            models.Index(fields=['owner', '-created_at']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.filename} ({self.owner.username})"

    def is_owner(self, user):
        """Check if user is the owner of this file."""
        return self.owner == user

    def is_allowed_user(self, user):
        """Check if user has access to this file."""
        return user in self.allowed_users.all()

    def has_access(self, user):
        """Check if user has any access to this file."""
        return self.is_owner(user) or self.is_allowed_user(user)
