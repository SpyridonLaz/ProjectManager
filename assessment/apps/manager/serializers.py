

from rest_framework.validators import UniqueValidator

from assessment.apps.manager.models import Project, Task, Tag, Status


from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers

from assessment.apps.manager.validators import UniqueTitlePerProjectValidator, IsFutureDateValidator, \
    OutOfTimeRangeValidator, LessThanParentDueDateValidator


class ProjectSerializer(serializers.ModelSerializer):
    """List,Retrieve"""
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
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
                  'is_public', 'progress']

        read_only_fields = ['id', 'owner', 'progress', 'status']






class TaskSerializer(serializers.ModelSerializer):

    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    due_date = serializers.DateTimeField(validators=[IsFutureDateValidator(hours=1), ])
    progress = serializers.DecimalField(max_digits=3,
                                        decimal_places=2,
                                        validators=[MinValueValidator(0), MaxValueValidator(1)])
    title = serializers.CharField(max_length=200,validators=[UniqueValidator(queryset=Task.objects.all(),),])

    tags =  serializers.SlugRelatedField(  slug_field="name", many=True, queryset=Tag.objects.all()  )

    class Meta:
        model = Task
        unique_together = ('project', 'title',)
        fields = ('project','title','progress', 'description',
                   'due_date', 'tags')
        read_only_fields = ['id',]

    def to_representation(self, instance):

        data = super().to_representation(instance)
        data['parent'] = ProjectSerializer(instance.project).data
        return data

    # def validate_title(self, value):
    #     self.initial.is_valid()
    #     UniqueTitlePerProjectValidator(value, self.data['parent'])
    #     return value
    #
    # def validate_due_date(self, value):
    #     LessThanParentDueDateValidator(value, parent=self.data['parent'])
    #     return value
    def to_internal_value(self, data):
        """
        This method is used to create tags if they don't exist.
        The format is a list of strings(tags)
        """
        raw_tags = data.get('tags', [])
        _t = []
        for tag in raw_tags:
            try:
                obj = Tag.objects.get(name=tag)
                _t.append(obj)
            except Tag.DoesNotExist as e:
                obj = Tag.objects.create(name=tag)
                _t.append(obj)
            except Exception as e:
                continue
        data['tags'] = _t
        return super(TaskSerializer, self).to_internal_value(data)

    def update(self, instance, validated_data):
        validated_project = validated_data['project']

        new_task =super().update(instance, validated_data)
        if validated_data['progress'] == 1:
            """
            If the task is completed, the parent project: progress , status
            fields are updated accordingly
            """
            validated_data['status'] = Status.COMPLETED
            completed_tasks = Task.objects.filter(project=validated_data['project'],progress__exact=1).count()
            total_tasks = Task.objects.filter(project=validated_data['project']).count()

            _prog =  round(completed_tasks/total_tasks,2,)
            data={'progress': _prog}
            if _prog == 1:
                data['status'] = Status.COMPLETED
            parent = ProjectSerializer(validated_project, data=data, partial=True)
            parent.progress = parent.is_valid()
            parent.save(update_fields=['progress'])

        return new_task
