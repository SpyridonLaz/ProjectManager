

from rest_framework.validators import UniqueValidator

from assessment.apps.manager.models import Project, Task, Tag, Status


from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers

from assessment.apps.manager.validators import  EnsureFutureDateValidator, OutOfTimeRangeValidator, CompleteByProgressValidator


class ProjectSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=200,
                                  validators=[UniqueValidator(queryset=Project.objects.all(),message="Title must be unique"),])
    progress = serializers.DecimalField(max_digits=3,
                                        decimal_places=2,
                                        validators=[MinValueValidator(0), MaxValueValidator(1)])
    due_date = serializers.DateTimeField(validators=[EnsureFutureDateValidator, ] )

    class Meta:
        model = Project
        fields = ['id', 'owner', 'title', 'description', 'due_date',
                  'is_public', 'progress']
        extra_kwargs = {
            'progress': {'read_only': True},
            'status': {'read_only': True},
        }






class TaskSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    title = serializers.CharField(max_length=200,)
    progress = serializers.DecimalField(max_digits=3,
                                        decimal_places=2,
                                        validators=[MinValueValidator(0), MaxValueValidator(1)])
    tags =  serializers.SlugRelatedField(  slug_field="name", many=True, queryset=Tag.objects.all()  )
    due_date = serializers.DateTimeField(validators=[EnsureFutureDateValidator, ] )

    class Meta:
        model = Task
        unique_together = ('project', 'title',)
        fields = ('project','title','progress', 'description',
                   'due_date', 'tags')
        extra_kwargs = {
            'status': {'read_only': True},
        }


    def validate_title(self, value):
        value = serializers.UniqueTogetherValidator(
            queryset=Task.objects.all(),
            fields=('title', 'project'),
            message={'details':"Title must be unique-test"}
        )
        project = self.initial_data['project']
        if Task.objects.filter(title=value,project = project).exists():
            raise serializers.ValidationError("Title must be unique")
        return value

    def to_internal_value(self, data):
        raw_tags = data.get('tags', [])
        _t=[]
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



    def validate(self, data):
        _id = self.initial_data['project']
        _obj = Project.objects.get(id=_id)

        OutOfTimeRangeValidator(days=1,)(data['due_date'],parent=_obj)
        CompleteByProgressValidator(_obj)



        OutOfTimeRangeValidator(_obj)(data['due_date'])
        if data['progress'] == 1:
            data['status'] = Status.COMPLETED
        return data




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
