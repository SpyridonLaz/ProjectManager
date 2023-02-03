from rest_framework import serializers

from assessment.apps.projects.models import Project, Status


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = [ 'id','owner', 'title', 'description', 'finish_date', 'is_public', 'status', 'progress' ]