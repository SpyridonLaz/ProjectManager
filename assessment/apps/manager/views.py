import json
import re

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from rest_framework import viewsets, status
from rest_framework.mixins import  UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS, AllowAny
from rest_framework.response import Response

from assessment import settings
from assessment.apps.manager.models import Project, Task
from assessment.apps.manager.permissions import IsOwner, IsVisible
from assessment.apps.manager.serializers import ProjectSerializer, TaskSerializer

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

    def get_permissions(self):
        if self.request.method in ['POST',]:
            self.permission_classes = [IsAuthenticated & TokenHasReadWriteScope]
        if self.request.method in ['PUT','PATCH','DELETE']:
            self.permission_classes = [IsOwner ]
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsVisible|IsOwner,]
        return super(ProjectViewSet, self).get_permissions()

#
# class ProjectUpdateViewSet(viewsets.GenericViewSet, UpdateModelMixin, DestroyModelMixin):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer
#
#     def get_permissions(self):
#         if self.request.method in ['PUT','PATCH','DELETE']:
#             self.permission_classes = [IsOwner ]
#         return super(ProjectUpdateViewSet, self).get_permissions()
#
#     def get_queryset(self):
#         queryset = Project.objects.all()
#         if self.request.user.is_authenticated:
#             queryset = Project.objects.filter(owner=self.request.user)
#         return queryset
#
#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#
#         return Response(serializer.data)


class TaskViewSet(ProjectViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

