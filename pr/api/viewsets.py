from rest_framework import viewsets
from api.models import *
from django.contrib.auth.models import User
from rest_framework.response import Response
from api.serializers import *
from cryptography.fernet import Fernet



class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PostingViewset(viewsets.ModelViewSet):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer

class StuDashboardViewset(viewsets.ModelViewSet):
    queryset = ApplicationStatus.objects.all()
    serializer_class = ForStatusSerializer
