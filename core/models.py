from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    student_id = models.CharField(max_length=20, unique=True, blank=True, null=True)  # 학번
    name = models.CharField(max_length=50, blank=True, null=True)  # 이름
    points = models.PositiveIntegerField(default=0)  # 리워드 시스템용 포인트

    def __str__(self):
        return f"{self.username} ({self.role})"

class TeacherRequest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} 님의 선생님 요청"

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    assigned_by = models.ForeignKey('core.User', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='tasks_received')
    is_complete = models.BooleanField(default=False)  # 작업 완료 여부
    created_at = models.DateTimeField(auto_now_add=True)
    
class TaskCompletion(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    student = models.ForeignKey(    
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='completed_tasks'
    )
