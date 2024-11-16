from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Task
from .forms import TaskForm, UserRegistrationForm

User = get_user_model()  # 사용자 정의 모델을 가져옵니다.

# 관리자 확인 함수 (람다로 대체 가능)
def is_admin(user):
    return user.is_staff  # 관리자인 경우 True 반환

# 관리자 대시보드 뷰
@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied. Only administrators can access this page.")
        return redirect('/')  # 홈 화면으로 리디렉션
    return render(request, 'admin_dashboard.html')

# 학생 대시보드 뷰
@login_required
def student_dashboard(request):
    tasks = Task.objects.filter(assigned_to=request.user, is_complete=False)  # 완료되지 않은 작업
    return render(request, 'core/student_dashboard.html', {'tasks': tasks})

# 로그인 후 리디렉션 뷰
@login_required
def after_login_view(request):
    if request.user.is_staff:
        return redirect('core:dashboard')  # 관리자 대시보드
    return redirect('core:student_dashboard')  # 학생 대시보드

# 작업 생성 뷰
@login_required
@user_passes_test(is_admin, login_url='/')
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_by = request.user
            task.save()
            return redirect('core:dashboard')
    else:
        form = TaskForm()
    return render(request, 'core/create_task.html', {'form': form})

# 작업 완료 표시 뷰
@login_required
def mark_task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.is_complete = True
    task.save()
    if request.user.is_staff:
        return redirect('core:dashboard')
    else:
        return redirect('core:student_dashboard')

# 회원가입 뷰
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.is_staff = False  # 기본적으로 학생 계정으로 설정
            user.save()
            login(request, user)  # 자동 로그인
            messages.success(request, f'회원가입이 완료되었습니다. {user.username}님 환영합니다!')
            return redirect('core:student_dashboard')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/forms/register.html', {'form': form})

# 대시보드 뷰 (학생/관리자 구분)
@login_required
def dashboard(request):
    if request.user.is_staff:
        return redirect('core:admin_dashboard')  # 관리자 대시보드
    else:
        return redirect('core:student_dashboard')  # 학생 대시보드

# 홈 뷰
def home(request):
    if 'logout' in request.GET:
        messages.success(request, "성공적으로 로그아웃되었습니다.")
    return render(request, 'core/home.html')

# 작업 보기 뷰
@login_required
def view_tasks(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'core/view_tasks.html', {'tasks': tasks})
