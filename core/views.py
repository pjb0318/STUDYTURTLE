# Django 기본 라이브러리
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from .models import TaskCompletion

# 프로젝트 및 앱 내부 모듈
from core.models import Task, User, TeacherRequest, Group
from core.forms import TaskForm, UserRegistrationForm, GroupForm, AddStudentToGroupForm

User = get_user_model()


class CustomLoginView(LoginView):
    def get_redirect_url(self):
        """로그인 후 리디렉션 URL 처리"""
        redirect_to = self.request.GET.get('next')  # `next` 매개변수 확인
        if redirect_to:
            return redirect_to
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
    students = User.objects.filter(role='student')
    teachers = User.objects.filter(role='teacher')
    pending_requests = TeacherRequest.objects.filter(is_approved=False)

    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')
        teacher_request = TeacherRequest.objects.get(id=request_id)

        if action == 'approve':
            teacher_request.is_approved = True
            teacher_request.user.role = 'teacher'
            teacher_request.user.save()
            teacher_request.save()
        elif action == 'reject':
            teacher_request.delete()

        return redirect('core:admin_dashboard')

    return render(request, 'core/dash/admin_dashboard.html', {
        'students': students,
        'teachers': teachers,
        'pending_requests': pending_requests,
    })


# 선생님 대시보드
@login_required
@user_passes_test(is_teacher, login_url='/')
def dashboard(request):
    # 현재 선생님이 할당한 과제
    tasks = Task.objects.select_related('group').filter(assigned_by=request.user)
    
    # 모든 학생
    students = User.objects.filter(role='student')
    
    # 선생님이 생성한 그룹
    groups_created = Group.objects.filter(creator=request.user)
    
    # 선택된 그룹의 ID가 요청에 포함된 경우 해당 그룹 정보 가져오기
    selected_group = None
    group_students = []
    if 'group_id' in request.GET:
        selected_group = Group.objects.filter(id=request.GET['group_id'], creator=request.user).first()
        if selected_group:
            group_students = selected_group.members.all()
    
    return render(request, 'core/dash/dashboard.html', {
        'tasks': tasks,
        'students': students,
        'groups_created': groups_created,  # 선생님이 생성한 그룹
        'selected_group': selected_group,  # 선택된 그룹
        'group_students': group_students,  # 선택된 그룹의 학생 목록
    })


@login_required
def student_dashboard(request):
    tasks = Task.objects.filter(group__members=request.user).exclude(taskcompletion__status='complete')
    selected_task = None
    if 'task_id' in request.GET:
        selected_task = Task.objects.filter(id=request.GET['task_id']).first()
    return render(request, 'core/dash/student_dashboard.html', {'tasks': tasks, 'selected_task': selected_task})


# 로그인 후 리디렉션
@login_required
def after_login_view(request):
    if request.user.role == 'admin':
        return redirect('core:admin_dashboard')
    elif request.user.role == 'teacher':
        return redirect('core:dashboard')
    elif request.user.role == 'student':
        return redirect('core:student_dashboard')
    return redirect('core:home')


# 작업 생성
@login_required
@user_passes_test(lambda u: u.role in ['admin', 'teacher'], login_url='/')
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, initial={'assigned_by': request.user})
        if form.is_valid():
            form.save()
            return redirect('core:dashboard')
        else:
            print("폼 검증 실패:", form.errors)
    else:
        form = TaskForm(initial={'assigned_by': request.user})
    return render(request, 'core/tasks/create_task.html', {'form': form})


# 작업 완료 표시
@login_required
def mark_task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    completion, created = TaskCompletion.objects.get_or_create(task=task, student=request.user)
    completion.status = 'complete'
    completion.save()
    if request.user.role == 'admin':
        return redirect('core:admin_dashboard')
    elif request.user.role == 'teacher':
        return redirect('core:dashboard')
    return redirect('core:student_dashboard')



# 회원가입
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.name = form.cleaned_data['name']
            user.student_id = form.cleaned_data['student_id']
            user.role = 'student'
            user.save()
            messages.success(request, f'{user.name}님, 회원가입이 완료되었습니다! 환영합니다!')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    # 실패 시 입력 데이터를 포함한 폼 다시 렌더링
    return render(request, 'registration/forms/register.html', {'form': form})

# 홈 뷰
def home(request):
    return render(request, 'core/home.html')


# 작업 보기
@login_required
def view_tasks(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'core/tasks/view_tasks.html', {'tasks': tasks})


# 선생님 역할 요청
@login_required
def request_teacher_role(request):
    if request.user.role != 'student':
        return redirect('/')
    if TeacherRequest.objects.filter(user=request.user).exists():
        return render(request, 'core/dash/request_teacher.html', {
            'error': '이미 요청을 보냈습니다.'
        })

    if request.method == 'POST':
        TeacherRequest.objects.create(user=request.user)
        return render(request, 'core/dash/request_teacher.html', {
            'success': '요청이 접수되었습니다. 관리자의 승인을 기다려주세요.'
        })

    return render(request, 'core/dash/request_teacher.html')


# 그룹 생성
@login_required
@user_passes_test(lambda u: u.role in ['admin', 'teacher'], login_url='/')
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:dashboard')
    else:
        form = GroupForm()
    return render(request, 'core/group/create_group.html', {'form': form})


@login_required
@user_passes_test(lambda u: u.role in ['admin', 'teacher'], login_url='/')  # 접근 권한 제한
def add_student_to_group(request, group_id):
    """
    그룹에 학생을 추가하는 뷰.
    """
    group = get_object_or_404(Group, id=group_id, creator=request.user)  # 그룹 확인
    if request.method == 'POST':
        student_id = request.POST.get('student_id')  # POST 데이터에서 학생 학번 가져오기
        student = get_object_or_404(User, student_id=student_id, role='student')  # 학생 확인
        group.members.add(student)  # 그룹에 학생 추가
        group.save()
        return redirect('core:dashboard')  # 성공 시 대시보드로 리디렉션
    return redirect('core:dashboard')  # GET 요청 시에도 대시보드로 리디렉션

@login_required
@user_passes_test(lambda u: u.role in ['admin', 'teacher'], login_url='/')  # 접근 권한 제한
def remove_student_from_group(request, group_id, student_id):
    """
    그룹에서 학생을 제거하는 뷰.
    """
    # 그룹 확인: 현재 사용자(선생님/관리자)가 생성한 그룹인지 확인
    group = get_object_or_404(Group, id=group_id, creator=request.user)
    
    # 학생 확인: 그룹 멤버인지 확인
    student = get_object_or_404(User, id=student_id, role='student')

    if request.method == 'POST':
        # 그룹 멤버에서 학생 제거
        group.members.remove(student)
        group.save()

        # 성공 메시지 추가 (선택 사항)
        return redirect('core:dashboard')  # 성공 후 대시보드로 리디렉션
    
    # POST 요청이 아니면 대시보드로 리디렉션
    return redirect('core:dashboard')

@login_required
@user_passes_test(lambda u: u.role in ['admin', 'teacher'], login_url='/')
def delete_task(request, task_id):
    """
    과제를 삭제하는 뷰.
    """
    task = get_object_or_404(Task, id=task_id, assigned_by=request.user)

    if request.method == 'POST':
        task.delete()
        return redirect('core:dashboard')

    return redirect('core:dashboard')

@login_required
@user_passes_test(lambda u: u.role in ['admin', 'teacher'], login_url='/')
def update_task(request, task_id):
    # 현재 사용자가 생성한 과제를 가져옴
    task = get_object_or_404(Task, id=task_id, assigned_by=request.user)

    if request.method == 'POST':
        # 폼 생성 시 'assigned_by' 초기 데이터를 전달
        form = TaskForm(request.POST, instance=task, initial={'assigned_by': request.user})
        if form.is_valid():
            form.save()  # 'assigned_by'는 폼 내부에서 설정됨
            return redirect('core:dashboard')
    else:
        # GET 요청일 경우에도 'assigned_by' 초기 데이터를 전달
        form = TaskForm(instance=task, initial={'assigned_by': request.user})

    return render(request, 'core/tasks/update_task.html', {'form': form, 'task': task})



