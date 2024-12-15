from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer, TaskInputSerializer


class TaskViewSet(ModelViewSet):
    """
    ViewSet for handling CRUD operations on Task model.
    """

    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        Returns the serializer class to be used for the request.

        Uses TaskInputSerializer for create, update, and partial_update actions.
        Uses TaskSerializer for other actions.
        """
        if self.action in ['create', 'update', 'partial_update']:
            return TaskInputSerializer
        return TaskSerializer

    def perform_update(self, serializer):
        """
        Performs update operation on a task.

        Raises PermissionDenied if the user is not the owner of the task.
        """
        task = self.get_object()
        if task.owner != self.request.user:
            raise PermissionDenied("You can only edit your tasks.")
        serializer.save()

    def perform_destroy(self, instance):
        """
        Performs delete operation on a task.

        Raises PermissionDenied if the user is not the owner of the task.
        """
        if instance.owner != self.request.user:
            raise PermissionDenied("You can only delete your tasks.")
        instance.delete()

    def perform_create(self, serializer):
        """
        Performs create operation on a task.

        Assigns the current user as the owner of the task.
        """
        serializer.save(owner=self.request.user)