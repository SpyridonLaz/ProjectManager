from django.shortcuts import render
from rest_framework import viewsets

from assessment.apps.projects.models import Project
from assessment.apps.projects.serializers import ProjectSerializer


# Create your project views here.




class ProjectViewSet(viewsets.ModelViewSet):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user )

    def get_object(self):

        queryset = self.get_queryset()
        obj = queryset.get(pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj



    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)



