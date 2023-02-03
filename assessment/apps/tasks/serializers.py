from rest_framework import serializers

from assessment.apps.tasks.models import Tag, Task



class TagSerializer(serializers.ModelSerializer):
    tag = serializers.CharField(max_length=50,required=False)

    class Meta:
        model = Tag
        fields = ('tag',)




class TaskSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True,required=False)
    class Meta:
        model = Task
        fields = ( 'title', 'description', 'project', 'progress', 'finish_date', 'tags',)




