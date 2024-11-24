# Django 기본 라이브러리
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model

# 프로젝트 및 앱 내부 모듈
from core.models import Task, User, TeacherRequest
from core.forms import TaskForm, UserRegistrationForm, GroupForm, AddStudentToGroupForm  # 통합된 forms.py에서 가져오기



User = get_user_model()


class CustomLoginView(LoginView):
    def get_redirect_url(self):
        """로그인 후 리디렉션 URL 처리"""
        redirect_to = self.request.GET.get('next')  # `next` 매개변수 확인
        if redirect_to:
            return redirect_to
        # 기본적으로 after-login 뷰로 리디렉션
        return resolve_url('core:after_login')
    
# 관리자 확인 함수
def is_admin(user):
    return user.role == 'admin'

# 선생님 확인 함수
def is_teacher(user):
    return user.role == 'teacher'


# 관리자 대시보드
@login_required
@user_passes_test(is_admin, login_url='/')
def admin_dashboard(request):
    # 학생 및 선생님 목록
    students = User.objects.filter(role='student')
    teachers = User.objects.filter(role='teacher')

    # 대기 중인 선생님 요청
    pending_requests = TeacherRequest.objects.filter(is_approved=False)

    # 요청 승인/거절 처리
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')
        teacher_request = TeacherRequest.objects.get(id=request_id)

        if action == 'approve':
            teacher_request.is_approved = True
            teacher_request.user.role = 'teacher'  # 역할 변경
            teacher_request.user.save()
            teacher_request.save()
        elif action == 'reject':
            teacher_request.delete()  # 요청 삭제

        return redirect('core:admin_dashboard')

    return render(request, 'core/admin_dashboard.html', {
        'students': students,
        'teachers': teachers,
        'pending_requests': pending_requests,
    })


# 선생님 대시보드
@login_required
@user_passes_test(is_teacher, login_url='/')
def dashboard(request):
    tasks = Task.objects.filter(assigned_by=request.user)
    students = User.objects.filter(role='student')
    return render(request, 'core/dashboard.html', {
        'tasks': tasks,
        'students': students,
    })

@login_required
def student_dashboard(request):
    # 학생이 속한 그룹의 미완료 작업 가져오기
    tasks = Task.objects.filter(group__members=request.user, taskcompletion__status='incomplete')
    return render(request, 'core/student_dashboard.html', {'tasks': tasks})

# 로그인 후 리디렉션
@login_required
def after_login_view(request):
    """로그인 후 사용자 역할에 따라 적합한 URL로 리디렉션"""
    if request.user.role == 'admin':
        return redirect('core:admin_dashboard')  # 관리자 대시보드로 이동
    elif request.user.role == 'teacher':
        return redirect('core:dashboard')  # 선생님 대시보드로 이동
    elif request.user.role == 'student':
        return redirect('core:student_dashboard')  # 학생 대시보드로 이동
    return redirect('core:home')  # 기본 홈으로 리디렉션

@login_required
@user_passes_test(lambda u: u.role in ['admin', 'teacher'], login_url='/')
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, initial={'assigned_by': request.user})
        if form.is_valid():
            form.save()
            return redirect('core:dashboard')  # 작업 생성 후 대시보드로 리디렉션
        else:
            print("폼 검증 실패:", form.errors)  # 디버깅 메시지
    else:
        form = TaskForm(initial={'assigned_by': request.user})
    return render(request, 'core/create_task.html', {'form': form})


# 작업 완료 표시 뷰
@login_required
def mark_task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.is_complete = True
    task.save()
    if request.user.role == 'admin':
        return redirect('core:admin_dashboard')
    elif request.user.role == 'teacher':
        return redirect('core:dashboard')
    return redirect('core:student_dashboard')

# 회원가입 뷰
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.name = form.cleaned_data['name']  # 이름 저장
            user.student_id = form.cleaned_data['student_id']  # 학번 저장
            user.role = 'student'  # 학생 계정으로 생성
            user.save()
            messages.success(request, f'{user.name}님, 회원가입이 완료되었습니다! 환영합니다!')
            return redirect('login')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/forms/register.html', {'form': form})

# 홈 뷰
def home(request):
    return render(request, 'core/home.html')

# 작업 보기 뷰
@login_required
def view_tasks(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'core/view_tasks.html', {'tasks': tasks})

@login_required
def request_teacher_role(request):
      # role이 'student'가 아닌 경우 접근 제한
    if request.user.role != 'student':
        return redirect('/')  # 403 에러 반환
    # 이미 요청한 경우
    if TeacherRequest.objects.filter(user=request.user).exists():
        return render(request, 'core/request_teacher.html', {
            'error': '이미 요청을 보냈습니다.'
        })

    # 요청 처리
    if request.method == 'POST':
        TeacherRequest.objects.create(user=request.user)
        return render(request, 'core/request_teacher.html', {
            'success': '요청이 접수되었습니다. 관리자의 승인을 기다려주세요.'
        })

    return render(request, 'core/request_teacher.html')

@login_required
@user_passes_test(lambda u: u.role in ['admin', 'teacher'], login_url='/')
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:dashboard')  # 그룹 생성 후 대시보드로 리디렉션
    else:
        form = GroupForm()
    return render(request, 'core/create_group.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.role in ['admin', 'teacher'], login_url='/')
def add_student_to_group(request):
    if request.method == 'POST':
        form = AddStudentToGroupForm(request.POST)
        if form.is_valid():
            group = form.cleaned_data['group']
            student = form.cleaned_data['student']
            group.members.add(student)  # 그룹에 학생 추가
            group.save()
            return redirect('core:dashboard')  # 완료 후 대시보드로 리디렉션
    else:
        form = AddStudentToGroupForm()
    return render(request, 'core/add_student_to_group.html', {'form': form})

