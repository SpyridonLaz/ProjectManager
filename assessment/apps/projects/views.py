from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from assessment.apps.projects.models import Project
from assessment.apps.projects.serializers import ProjectSerializer

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope


# Create your project views here.




class ProjectViewSet(viewsets.ModelViewSet):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated,]

    #def get_queryset(self):
       # user = self.request.user
        #return self.queryset.filter(user=user )

   # def get_object(self):

        #queryset = self.get_queryset()
       # obj = queryset.get(pk=self.kwargs['pk'])
       # self.check_object_permissions(self.request, obj)
       # return obj



    #def perform_create(self, serializer):
       # serializer.save(user=self.request.user)

  #  def perform_update(self, serializer):
     #   serializer.save(user=self.request.user)



    def list(self, request, *args, **kwargs):
        return Response(request.user,request.user.id,request.user.username,request.user.email)

