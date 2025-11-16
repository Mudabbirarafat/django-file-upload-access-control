
from django.urls import path
from .views import RegisterView, UploadFileView, ListFilesView, DownloadFileView, SignedURLView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('auth/register/', RegisterView.as_view()),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('files/upload/', UploadFileView.as_view()),
    path('files/', ListFilesView.as_view()),
    path('files/<uuid:pk>/download/', DownloadFileView.as_view()),
    path('files/<uuid:pk>/signed-url/', SignedURLView.as_view()),
]
