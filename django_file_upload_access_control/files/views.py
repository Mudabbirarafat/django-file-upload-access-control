
import os
import json
from io import BytesIO

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from django.conf import settings
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.http import FileResponse, Http404
from django.db import models

from cryptography.fernet import Fernet, InvalidToken

from .models import UploadedFile
from .serializers import UploadedFileSerializer, UserSerializer


signer = TimestampSigner()


def get_fernet():
    """Get Fernet cipher from settings."""
    key = settings.FERNET_KEY
    if not key:
        raise ValueError('FERNET_KEY not set in settings or .env')
    return Fernet(key.encode())


class RegisterView(generics.CreateAPIView):
    """User registration endpoint."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '').strip()

        if not username or not password:
            return Response(
                {'detail': 'username and password required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {'detail': 'user already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if len(password) < 8:
            return Response(
                {'detail': 'password must be at least 8 characters'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(username=username, password=password)
        return Response({
            'id': user.id,
            'username': user.username
        }, status=status.HTTP_201_CREATED)


class UploadFileView(generics.GenericAPIView):
    """File upload endpoint with encryption."""
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = UploadedFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        file_obj = request.FILES.get('file')
        share_with = request.data.get('share_with')

        if not file_obj:
            return Response(
                {'detail': 'file required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create UploadedFile instance
        filename = file_obj.name
        uploaded_file = UploadedFile.objects.create(
            owner=user,
            filename=filename
        )

        # Create directory structure
        rel_path = os.path.join('files', str(uploaded_file.id))
        full_dir = os.path.join(settings.MEDIA_ROOT, rel_path)
        os.makedirs(full_dir, exist_ok=True)

        target_path = os.path.join(full_dir, filename)

        # Encrypt and save file
        try:
            raw_data = file_obj.read()
            fernet = get_fernet()
            encrypted_data = fernet.encrypt(raw_data)

            with open(target_path, 'wb') as output_file:
                output_file.write(encrypted_data)

            # Update FileField path
            uploaded_file.file.name = os.path.join(rel_path, filename)

            # Handle share_with users
            if share_with:
                try:
                    users_list = json.loads(share_with)
                    for username in users_list:
                        try:
                            share_user = User.objects.get(username=username)
                            uploaded_file.allowed_users.add(share_user)
                        except User.DoesNotExist:
                            pass
                except (json.JSONDecodeError, TypeError):
                    pass

            uploaded_file.save()
            return Response(
                UploadedFileSerializer(uploaded_file).data,
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            # Clean up on error
            uploaded_file.delete()
            if os.path.exists(target_path):
                os.remove(target_path)
            return Response(
                {'detail': f'Upload failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ListFilesView(generics.ListAPIView):
    """List files owned by or shared with the user."""
    serializer_class = UploadedFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return UploadedFile.objects.filter(
            models.Q(owner=user) | models.Q(allowed_users=user)
        ).distinct().order_by('-created_at')


class DownloadFileView(generics.GenericAPIView):
    """Download file with optional signed token authentication."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        token = request.query_params.get('token')

        try:
            uploaded_file = UploadedFile.objects.get(pk=pk)
        except UploadedFile.DoesNotExist:
            raise Http404('File not found')

        # Validate access
        if token:
            # Validate signed token for public/time-limited access
            try:
                data = signer.unsign(token, max_age=3600)
                if data != f"file:{pk}":
                    return Response(
                        {'detail': 'invalid token'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            except SignatureExpired:
                return Response(
                    {'detail': 'token expired'},
                    status=status.HTTP_403_FORBIDDEN
                )
            except BadSignature:
                return Response(
                    {'detail': 'bad signature'},
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            # Check user permissions
            user = request.user
            if uploaded_file.owner != user and user not in uploaded_file.allowed_users.all():
                return Response(
                    {'detail': 'permission denied'},
                    status=status.HTTP_403_FORBIDDEN
                )

        # Serve file
        full_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.file.name)
        if not os.path.exists(full_path):
            raise Http404('File not found on disk')

        try:
            fernet = get_fernet()
            with open(full_path, 'rb') as input_file:
                encrypted_data = input_file.read()
                decrypted_data = fernet.decrypt(encrypted_data)

            # Return as file download
            buffer = BytesIO(decrypted_data)
            response = FileResponse(
                buffer,
                as_attachment=True,
                filename=uploaded_file.filename
            )
            return response

        except InvalidToken:
            return Response(
                {'detail': 'decryption error - invalid token'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {'detail': f'decryption error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SignedURLView(generics.GenericAPIView):
    """Generate time-limited signed URLs for file downloads."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            uploaded_file = UploadedFile.objects.get(pk=pk)
        except UploadedFile.DoesNotExist:
            raise Http404('File not found')

        # Only file owner can create signed URLs
        if uploaded_file.owner != request.user:
            return Response(
                {'detail': 'only owner can create signed url'},
                status=status.HTTP_403_FORBIDDEN
            )

        expires_in = int(request.query_params.get('expires', '300'))
        value = f"file:{pk}"
        token = signer.sign(value)

        return Response({
            'url': f"/api/files/{pk}/download/?token={token}",
            'expires_in': expires_in
        }) 
