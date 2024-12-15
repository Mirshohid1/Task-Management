from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User


class Task(models.Model):
    """
    Represents a task assigned to a user.

    Attributes:
        title (str): The title of the task, must be at least 3 characters long.
        description (str): A detailed description of the task, must be at least 12 characters long.
        status (str): The current status of the task. Can be 'pending', 'in_progress', or 'completed'.
        created_at (datetime): The timestamp when the task was created.
        owner (User): The user who owns the task.
    """

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)],
    )
    description = models.TextField(
        validators=[MinLengthValidator(12)],
    )
    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default='pending',
        validators=[MinLengthValidator(6)],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    def save(self, *args, **kwargs):
        """
        Save the task to the database after cleaning and formatting its fields.

        - Strips leading and trailing whitespace from the title and description.
        - Converts the title to title case.
        - Capitalizes the first letter of the description.
        """
        self.title = self.title.strip().title()
        self.description = self.description.strip().capitalize()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.status})"