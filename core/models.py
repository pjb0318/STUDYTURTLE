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


class Group(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)  # 그룹 설명 (선택 사항)
    members = models.ManyToManyField(User, related_name='group_memberships')  # 그룹 멤버

    def __str__(self):
        return self.name




class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='tasks')  # 그룹과 연결
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE)  # 과제를 생성한 사용자
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TaskCompletion(models.Model):  # 이름을 기존대로 유지
    STATUS_CHOICES = (
        ('incomplete', '미완료'),
        ('in_progress', '진행 중'),
        ('complete', '완료'),
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='task_completions'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='incomplete')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.username} - {self.task.title} ({self.status})"
    
    