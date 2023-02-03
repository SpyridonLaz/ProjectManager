from rest_framework import serializers

from assessment.apps.projects.models import Project, Status


class ProjectSerializer(serializers.ModelSerializer):


    class Meta:
        model = Project
        fields = [ 'user', 'title', 'description', 'start_date', 'end_date', ]