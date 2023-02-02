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
        return Project.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

