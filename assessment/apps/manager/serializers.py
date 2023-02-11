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






class TaskSerializer(serializers.ModelSerializer):

    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    due_date = serializers.DateTimeField(validators=[IsFutureDateValidator(hours=1), ])
    progress = serializers.DecimalField(max_digits=3,
                                        decimal_places=2,
                                        validators=[MinValueValidator(0), MaxValueValidator(1)])
    title = serializers.CharField(max_length=200,)

    tags =  serializers.SlugRelatedField(  slug_field="name", many=True, queryset=Tag.objects.all()  )

    class Meta:
        depth = 2
        model = Task
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Task.objects.all(),
                fields=('title', 'project'),
            )
        ]
        fields = ('project','title','tags','progress', 'description',
                   'due_date', )
        read_only_fields = ['id','project']



    def validate_due_date(self, value):

        LessThanParentDueDateValidator(value, self.context.get('parent'))
        return value


    def to_internal_value(self, data):
        """
        This method is used to create tags if they don't exist.
        The format is a list of strings(tags)
        """

        print("START")
        #self.parent_obj = self.context.get('parent')

        raw_tags = data.get('tags', [])
        print("RAW",raw_tags)
        _t = []
        for tag in raw_tags:
            print("TAG",tag)
            try:
                _t.append(Tag.objects.get_or_create(name=tag)[0])
            except Exception as e:
                raise ValidationError({'detail': "Tag PARSER PROBLEM"})
        data['tags'] = _t
        print(data['tags'])
        print("DATA",data)
        return super(TaskSerializer, self).to_internal_value(data)

    def update(self, instance, validated_data):

        # validated_data['tags'] =  [Tag.objects.get_or_create(name=tag)[0] for tag in validated_data.get('tags', [])]
        print("validated_data",validated_data)

        print("validated_data",validated_data)
        project =  instance.project


        new_task =super().update(instance,validated_data,)
        if validated_data['progress'] == 1:
            print("VALIDATED:  ",project)
            """
            If the task is completed, the parent project: progress , status
            fields are updated accordingly
            """
            validated_data['status'] = Status.COMPLETED
            completed_tasks = Task.objects.filter(project=project,progress__exact=1).count()
            total_tasks = Task.objects.filter(project=project).count()
            _prog =  round(completed_tasks+1/total_tasks,2,)
            print("PROGRESS",_prog)
            data={}
            if _prog == 1:
                data['status'] = Status.COMPLETED
                data['progress'] = _prog
            parent = ProjectSerializer(project, data=data, partial=True)
            print("PARENT",parent)
            parent.progress = parent.is_valid()
            parent.save(update_fields=['progress'])

        return new_task




