import datetime

from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from assessment.apps.manager.models import Project, Task, Tag, Status


from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers

from assessment.apps.manager.validators import UniqueTitlePerProjectValidator, IsFutureDateValidator, \
    OutOfTimeRangeValidator, LessThanParentDueDateValidator


class ProjectSerializer(serializers.ModelSerializer):
    """List,Retrieve"""
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    due_date = serializers.DateTimeField(validators=[IsFutureDateValidator(days=60), ])


    class Meta:
        model = Project
        fields = ['id', 'owner', 'title', 'description', 'due_date',
                  'is_public', 'progress','status']

    def validate_due_date(self, value):
        return value


class ProjectCUDSerializer(serializers.ModelSerializer):
    """Create,Update"""

    title = serializers.CharField(max_length=200,
                                  validators=[UniqueValidator(queryset=Project.objects.all(),),])
    progress = serializers.DecimalField(max_digits=3,
                                        decimal_places=2,
                                        validators=[MinValueValidator(0), MaxValueValidator(1)])


    due_date = serializers.DateTimeField(validators=[IsFutureDateValidator(days=60), ])

    class Meta:
        model = Project
        fields = ['id', 'owner', 'title', 'description', 'due_date',
                  'is_public', 'progress','status']

        read_only_fields = ['id',  'progress', ]



class TaskCreateSerializer(serializers.ModelSerializer):
    """Create"""
    id = serializers.IntegerField(read_only=True)
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    due_date = serializers.DateTimeField(validators=[IsFutureDateValidator(hours=1), ])
    progress = serializers.DecimalField(max_digits=3,
                                        decimal_places=2,
                                        validators=[MinValueValidator(0), MaxValueValidator(1)])
    title = serializers.CharField(max_length=200, )
    tags =  serializers.SlugRelatedField(  slug_field="name", many=True, queryset=Tag.objects.all()  )
    status = serializers.ChoiceField(choices=Status.choices, default=Status.IN_PROGRESS,allow_blank=True)

    class Meta:
        depth = 1
        model = Task
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Task.objects.all(),
                fields=('title', 'project'),
            )
        ]
        fields = ('id','project','title','tags','progress', 'description',
                   'due_date','status' )

    def validate_due_date(self, value:datetime):
        LessThanParentDueDateValidator(value, self.context.get('parent'))

        return value

    def to_internal_value(self, data):
        """
        We create tags if they don't exist
        so that we can create many to many relationships
        on the fly.
        """
        data['tags'] = [Tag.objects.get_or_create(name=tag)[0] for tag in data.get('tags', [])]
        return super(TaskCreateSerializer, self).to_internal_value(data)


class TaskUpdateSerializer(TaskCreateSerializer):
    """Update"""
    class Meta:
        model = Task

        fields = ('tags','progress', 'description',
                   'due_date', 'status' )
        read_only_fields = ['id','project']

    def update(self, instance, validated_data):
        project =  instance.project
        task = super().update(instance, validated_data, )
        if validated_data['progress'] == 1:
            """
            If the task is completed, then task's status is updated and 
            also the parent project: progress , status
            fields are updated accordingly
            """
            validated_data['status'] = Status.COMPLETED.value
            task= super().update(task, validated_data, )

            # calculating the progress of the parent project
            completed_tasks = Task.objects.filter(project=project,progress__exact=1).count()
            total_tasks = Task.objects.filter(project=project).count()
            _prog =  round(completed_tasks/total_tasks,2,)

            data = {}
            if _prog == 1:
            # if all tasks are completed, then the project status becomes completed

                data['status'] = Status.COMPLETED.value
            # updating progress,status of parent project
            data['progress'] = _prog
            parent = ProjectSerializer(project, data=data, partial=True)
            parent.progress = parent.is_valid()
            parent.save(update_fields=['progress','status'])

        return task


