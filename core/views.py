from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm, UserRegistrationForm
from .decorators import admin_only
from django.contrib.auth.models import User
from django.contrib.auth import login, get_user_model
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm



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
    if request.user.is_staff:
        # 관리자인 경우
        return render(request, 'admin_dashboard.html')
    else:
        # 일반 사용자(학생)인 경우
        return render(request, 'user_dashboard.html')
    
def mark_task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id)  # `Task` 모델에서 작업 가져오기
    task.is_complete = True  # 작업 완료 표시
    task.save()  # 변경 저장

    # 학생은 학생 대시보드로, 관리자는 관리자 대시보드로 리디렉션
    if request.user.is_staff:
        return redirect('core:dashboard')
    else:
        return redirect('core:student_dashboard')


from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm  # 사용자 정의 폼

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # User 객체를 폼에서 생성
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.is_staff = False  # 회원가입 시 무조건 학생 계정으로 설정
            user.save()  # 데이터베이스에 저장

            # 자동 로그인
            login(request, user)
            messages.success(request, f'회원가입이 완료되었습니다. {user.username}님 환영합니다!')
            return redirect('student_dashboard')  # 학생 대시보드로 리디렉션
        else:
            # 오류 메시지를 추가
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/forms/register.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html', {'user': request.user})

def home(request):
    if 'logout' in request.GET:
        messages.success(request, "성공적으로 로그아웃되었습니다.")
    return render(request, 'core/home.html')

@login_required
def student_dashboard(request):
    # 학생에게 할당된 작업 데이터를 가져옵니다.
    tasks = Task.objects.filter(assigned_to=request.user, is_complete=False)  # 완료되지 않은 작업
    return render(request, 'core/student_dashboard.html', {'tasks': tasks})
@login_required
def student_dashboard(request):
    return render(request, 'core/student_dashboard.html')  # 학생 대시보드 템플릿

@login_required
def view_tasks(request):
    # 작업 데이터를 가져와 템플릿에 전달
    tasks = []  # 예: 작업 데이터를 가져오는 로직 추가
    return render(request, 'core/view_tasks.html', {'tasks': tasks})