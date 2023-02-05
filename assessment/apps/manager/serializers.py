from rest_framework.validators import UniqueValidator

from assessment.apps.manager.models import Project, Task,  Tag

from datetime import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers



class ProjectSerializer(serializers.ModelSerializer):
    progress = serializers.DecimalField(max_digits=3,
                                        decimal_places=2,
                                        validators=[MinValueValidator(0), MaxValueValidator(1)])
    due_date = serializers.DateTimeField()

    class Meta:
        model = Project
        fields = ['id', 'owner', 'title', 'description', 'due_date',
                  'is_public', 'progress']
        extra_kwargs = {
            'progress': {'read_only': True},
            'status': {'read_only': True},
        }






class TaskSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=200,)
    progress = serializers.DecimalField(max_digits=3,
                                        decimal_places=2,
                                        validators=[MinValueValidator(0), MaxValueValidator(1)])
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    tags =  serializers.SlugRelatedField(  slug_field="name", many=True, queryset=Tag.objects.all()  )
    due_date = serializers.DateTimeField()
    class Meta:
        model = Task
        fields = ('title', 'description', 'project',
                  'progress', 'due_date', 'tags')
        extra_kwargs = {
            'status': {'read_only': True},
        }

    #
    def to_internal_value(self, data):
        raw_tags = data.get('tags', [])
        _t=[]
        for tag in raw_tags:
            try:
                obj = Tag.objects.get(name=tag)
                _t.append(obj)
            except Tag.DoesNotExist as e:
                print(e)
                obj = Tag.objects.create(name=tag)
                _t.append(obj)
            except Exception as e:
                print(e)
                continue
        data['tags'] = _t
        print(data['tags'])
        return super(TaskSerializer, self).to_internal_value(data)

    #
    #
    # def validate(self, data):
    #
    #     _id = self.initial_data['project']
    #     _obj = Project.objects.get(id=_id)
    #     TaskOverdueValidator(_obj)(data['due_date'])
    #     if data['progress'] == 1:
    #         data['status'] = Status.COMPLETED
    #
    #
    #     return data
    #



    # def create(self, validated_data):
    #     """ kai EDW EINAI GIA MANIPULATION
    #
    #     You should use an object wide validation (validate()),
    #     since validate_date will never be called since date is not a field on the serializer.
    #
    #     """
    #     if datetime.now().date() > validated_data['due_date'].date():
    #         raise serializers.ValidationError("Due date must be a future date.")
    #     if validated_data['progress'] == 100:
    #         validated_data['status'] = Status.COMPLETED
    #
    #     task = Task.objects.create(**validated_data)
    #     return task
