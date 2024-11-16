from django import forms
from .models import Task
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()  # 사용자 정의 모델 가져오기

# Task 모델 폼
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'assigned_by']  # Task 모델의 필드
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'assigned_by': forms.Select(attrs={'class': 'form-control'}),
        }

# 사용자 등록 폼
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': '사용자 이름',
            'email': '이메일 주소',
            'password1': '비밀번호',
            'password2': '비밀번호 확인',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("이미 등록된 이메일입니다.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'  # 기본적으로 학생으로 설정
        if commit:
            user.save()
        return user
