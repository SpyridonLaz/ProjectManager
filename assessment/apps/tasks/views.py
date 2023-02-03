from rest_framework import viewsets

from assessment.apps.tasks.models import Task
from assessment.apps.tasks.serializers import TaskSerializer


# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pass




