
from rest_framework import serializers
from .models import UploadedFile
from django.contrib.auth.models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']
class UploadedFileSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    allowed_users = serializers.SlugRelatedField(slug_field='username', many=True, queryset=User.objects.all(), required=False)
    class Meta:
        model = UploadedFile
        fields = ['id','owner','filename','created_at','allowed_users','encrypted']
