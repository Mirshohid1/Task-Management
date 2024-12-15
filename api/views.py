from rest_framework.viewsets import ModelViewSet
from .models import Task
from .serializers import TaskSerializer, TaskInputSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TaskInputSerializer
        return TaskSerializer
