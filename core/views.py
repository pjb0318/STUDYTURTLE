from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm, UserRegistrationForm
from .decorators import admin_only

from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, get_user_model
User = get_user_model()  # 사용자 정의 모델을 가져옵니다.

@login_required
@admin_only
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_by = request.user
            task.save()
            return redirect('dashboard')
    else:
        form = TaskForm()
    return render(request, 'core/create_task.html', {'form': form})


def home(request):
    return render(request, 'core/home.html')

def dashboard(request):
    return render(request, 'core/dashboard.html')

def mark_task_complete(request, task_id):
    # `Task` 모델에서 주어진 `task_id`로 작업을 가져옵니다.
    task = get_object_or_404(Task, id=task_id)
    task.is_complete = True  # 작업을 완료로 표시
    task.save()  # 변경사항 저장
    return redirect('dashboard')  # 완료 후 대시보드로 리디렉션



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # User 객체를 폼에서 생성
            user = form.save(commit=False)  # commit=False로 일단 객체 생성
            user.email = form.cleaned_data['email']  # 이메일 설정
            user.save()  # 데이터베이스에 저장

            # 자동 로그인
            login(request, user)
            return redirect('dashboard')  # 로그인 후 대시보드로 리디렉션
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/forms/register.html', {'form': form})
