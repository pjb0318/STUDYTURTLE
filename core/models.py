from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)



from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()  # 설명 필드 추가
    due_date = models.DateField()  # 마감일 필드 추가
    assigned_by = models.ForeignKey('core.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    
class TaskCompletion(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    student = models.ForeignKey(    
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='completed_tasks'
    )


