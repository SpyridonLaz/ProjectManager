import datetime
from rest_framework.validators import UniqueValidator
from assessment.apps.manager.models import Project, Task, Tag, Status
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers
from assessment.apps.manager.validators import IsFutureDateValidator, LessThanParentDueDateValidator









class AbstractSerializer(serializers.ModelSerializer):
    """Base serializer for both project and task models"""
    id = serializers.IntegerField(read_only=True)
    description = serializers.CharField(max_length=500, allow_blank=True)
    status = serializers.ChoiceField(choices=Status.choices, default=Status.IN_PROGRESS, allow_blank=True)
    due_date = serializers.DateTimeField(validators=[IsFutureDateValidator(), ])
    progress = serializers.DecimalField(max_digits=3,
                                        decimal_places=2,
                                        validators=[MinValueValidator(0), MaxValueValidator(1)])
    class Meta:
        abstract = True
    


class ProjectSerializer(AbstractSerializer):
    """list, retrieve,create,"""
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    
    title = serializers.CharField(max_length=200,
                                  validators=[UniqueValidator(queryset=Project.objects.all(), ), ])
    is_public = serializers.BooleanField(default=False)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'due_date',
                  'is_public', 'progress', 'status', 'owner']

    def validate_due_date(self, value):
        return value


class ProjectUpdateSerializer(serializers.ModelSerializer):
    """Update, partial_update"""
    
    class Meta:
        model = Project
        fields = ['description', 'due_date',
                  'is_public', 'progress', 'status']

        read_only_fields = ['id', 'title', 'owner']

    def update(self, instance, validated_data):
        updated_project = super().update(instance, validated_data, )
        if validated_data['status'] in (2, 4):
            """
            If the task is canceled or set as incomplete, 
            then the status of it's tasks will be updated accordingly
            """
            tasks = Task.objects.filter(project=self.instance.id)
            tasks = [TaskUpdateSerializer(task, data={'status': Status.CANCELED}, partial=True) for task in tasks]
            [task.is_valid() for task in tasks]
            [task.save() for task in tasks]
        return updated_project


class TaskSerializer(AbstractSerializer):
    """list, retrieve,create,"""
    id = serializers.IntegerField(read_only=True)
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
 

    title = serializers.CharField(max_length=200, )
    tags = serializers.SlugRelatedField(slug_field="name", many=True, queryset=Tag.objects.all())

    class Meta:
        depth = 1
        model = Task
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Task.objects.all(),
                fields=('title', 'project'), )
        ]
        fields = ('id', 'project', 'title', 'tags', 'progress', 'description',
                  'due_date', 'status')

    def validate_due_date(self, value: datetime):
        LessThanParentDueDateValidator(value, self.context.get('parent'))
        return value

    def to_internal_value(self, data):
        """
        We create tags if they don't exist
        so that we can create many to many relationships
        on the fly.
        """
        data['tags'] = [Tag.objects.get_or_create(name=tag)[0] for tag in data.get('tags', [])]
        return super(TaskSerializer, self).to_internal_value(data)


class TaskUpdateSerializer(TaskSerializer):
    """Update"""

    class Meta:
        model = Task
        fields = ('tags', 'progress', 'description',
                  'due_date', 'status')
        read_only_fields = ['id', 'project']

    def update(self, instance, validated_data):
        project = instance.project
        updated_task = super().update(instance, validated_data, )
        if validated_data.get('progress') == 1:
            """
            If the task is completed, then task's status is updated and 
            also the parent project: progress , status
            fields are updated accordingly
            """
            validated_data['status'] = Status.COMPLETED.value
            updated_task = super().update(updated_task, validated_data, )

            # calculating the progress of the parent project
            completed_tasks = Task.objects.filter(project=project, progress__exact=1).count()
            total_tasks = Task.objects.filter(project=project).count()
            _prog = round(completed_tasks / total_tasks, 2, )

            data = {}
            if _prog == 1:
                # if all tasks are completed, then the project status becomes completed

                data['status'] = Status.COMPLETED.value
            # updating progress,status of parent project
            data['progress'] = _prog
            parent = ProjectSerializer(project, data=data, partial=True)
            parent.progress = parent.is_valid()
            parent.save(update_fields=['progress', 'status'])

        return updated_task