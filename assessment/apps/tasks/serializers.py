from datetime import datetime,time

from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers

from assessment.apps.projects.models import Status
from assessment.apps.tasks.models import  Task




class Tag(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('tag',)

class TaskSerializer(serializers.ModelSerializer):
    progress = serializers.DecimalField(max_digits=5,
                                        decimal_places=2,
                                        validators=[MinValueValidator(0), MaxValueValidator(100)] )
    lol = serializers.CharField(source='tag', read_only=True)
    class Meta:
        model = Task
        fields = ( 'title', 'description', 'project', 'progress', 'due_date', 'tag','lol')


    def create(self, validated_data):
        """  EDW EINAI GIA MANIPULATION

        You should use an object wide validation (validate()),
        since validate_date will never be called since date is not a field on the serializer.

        """

        if datetime.now().date() > validated_data['due_date'].date():
            raise serializers.ValidationError("Due date must be in the future")
        if validated_data['progress'] == 100:
            validated_data['status'] = Status.COMPLETED




        task = Task.objects.create(**validated_data)
        return task



