from rest_framework import serializers

from assessment.apps.tasks.models import Tag, Task

class TagSerializer(serializers.ModelSerializer):
    tag = serializers.CharField(max_length=50,required=False)
    class Meta:
        model = Tag
        fields = ('tag',)
class TaskSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Task
        fields = ( 'title', 'description', 'project', 'progress', 'finish_date', 'tags',)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        task = Task.objects.create(**validated_data)
        for tag in tags:
            task.tags.add(tag)
        return task

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.project = validated_data.get('project', instance.project)
        instance.progress = validated_data.get('progress', instance.progress)
        instance.finish_date = validated_data.get('finish_date', instance.finish_date)
        instance.save()
        instance.tags.clear()
        for tag in tags:
            instance.tags.add(tag)
        return instance





