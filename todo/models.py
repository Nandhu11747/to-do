from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assigned_tasks")

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_tasks")

    completed = models.BooleanField(default=False)

    due_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
