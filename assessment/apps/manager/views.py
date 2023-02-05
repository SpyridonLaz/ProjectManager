import json
import re

from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from assessment import settings
from assessment.apps.manager.models import Project, Task
from assessment.apps.manager.permissions import IsProjectOwner, ViewIsPublic, ObjectStatus
from assessment.apps.manager.serializers import ProjectSerializer, TaskSerializer
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from django.core.cache.backends.base import DEFAULT_TIMEOUT

from assessment.apps.manager.validators import CompleteByExpirationValidator

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    def get_queryset(self):
        queryset = Project.objects.all()
        return queryset

    @method_decorator(cache_page(CACHE_TTL))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
        if self.request.method in SAFE_METHODS:
            self.permission_classes += [ViewIsPublic | IsProjectOwner, ]
        else:
            self.permission_classes += [IsProjectOwner,ObjectStatus, ]
        return super(ProjectViewSet, self).get_permissions()

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            CompleteByExpirationValidator(obj)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        return super(ProjectViewSet, self).update(request, *args, **kwargs)


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @method_decorator(cache_page(CACHE_TTL))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
        if self.request.method in SAFE_METHODS:
            self.permission_classes += [ViewIsPublic | IsProjectOwner, ]
        else:
            self.permission_classes += [IsProjectOwner,ObjectStatus,]
        return super(TaskViewSet, self).get_permissions()
