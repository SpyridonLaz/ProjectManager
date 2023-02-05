from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers

from assessment.apps.projects.models import Project, Status


class ProjectSerializer(serializers.ModelSerializer):
    progress = serializers.DecimalField(max_digits=5,
                                        decimal_places=2,

                                        validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        model = Project
        fields = [ 'owner', 'title',
                   'description', 'due_date',
                   'is_public', 'progress' ]
        extra_kwargs = {
            'status': {'read_only': True}
        }


