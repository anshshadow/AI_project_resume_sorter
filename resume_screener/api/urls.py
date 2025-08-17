from django.urls import path
from .views import RegisterView, JobDescriptionListCreateView, JobDescriptionDetailView, ResumeUploadView, ResumeListView, ResumeDetailView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('jobs/', JobDescriptionListCreateView.as_view(), name='job-list-create'),
    path('jobs/<int:pk>/', JobDescriptionDetailView.as_view(), name='job-detail'),
    path('jobs/<int:job_id>/upload/', ResumeUploadView.as_view(), name='resume-upload'),
    path('jobs/<int:job_id>/resumes/', ResumeListView.as_view(), name='resume-list'),
    path('resumes/<int:pk>/', ResumeDetailView.as_view(), name='resume-detail'),
]
