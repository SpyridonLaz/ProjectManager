from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.viewsets import  ModelViewSet

from assessment import settings
from assessment.apps.manager.models import Project, Task
from assessment.apps.manager.permissions import IsOwner, IsPublic, ObjectStatus
from assessment.apps.manager.serializers import ProjectSerializer, TaskSerializer
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from django.core.cache.backends.base import DEFAULT_TIMEOUT


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ProjectSerializer
        return ProjectSerializer


    def get_object(self):
        return Project.objects.get(id=self.kwargs['pk'])

    @method_decorator(cache_page(CACHE_TTL))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
        if self.request.method in SAFE_METHODS:
            self.permission_classes += [IsPublic | IsOwner, ]
        else:
            self.permission_classes += [IsOwner, ]
        return super(ProjectViewSet, self).get_permissions()




class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()

    @method_decorator(cache_page(CACHE_TTL))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def get_serializer_class(self):
        if self.action == SAFE_METHODS:
            return TaskSerializer
        return TaskSerializer

    # def get_serializer_context(self):
    #     """
    #         Inject the parent project into the serializer context.
    #     """
    #     context = super().get_serializer_context()
    #
    #     if self.action not in SAFE_METHODS:
    #         context.update({'parent': Project.objects.get(id=_id)})
    #         print(context.get('parent'))
    #     return context


    def get_permissions(self):
        self.permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
        if self.request.method in SAFE_METHODS:
            self.permission_classes += [IsPublic | IsOwner, ]
        else:
            self.permission_classes += [IsOwner, ObjectStatus, ]
        return super(TaskViewSet, self).get_permissions()
