import json
import re

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.mixins import  UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response

from assessment import settings
from assessment.apps.projects.models import Project
from assessment.apps.projects.permissions import IsOwner, IsVisible
from assessment.apps.projects.serializers import ProjectSerializer

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from oauth2_provider.models import AccessToken

from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

# Create your project views here.



class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @method_decorator(cache_page(CACHE_TTL))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Project.objects.all()
        if self.request.user.is_authenticated:
            queryset = Project.objects.filter(owner=self.request.user)
        return queryset

    def get_permissions(self):
        if self.request.method in ['POST',]:
            self.permission_classes = [IsAuthenticated & TokenHasReadWriteScope]
        if self.request.method in ['PUT','PATCH','DELETE']:
            self.permission_classes = [IsOwner ]
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsVisible|IsOwner,]

        return super(ProjectViewSet, self).get_permissions()