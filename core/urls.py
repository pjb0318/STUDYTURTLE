from django.urls import path
from core import views
from django.contrib.auth import views as auth_views  # Django 기본 인증 뷰 임포트
from core.views import request_teacher_role

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),  # 홈 페이지
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),  # 관리자 대시보드
    path('dashboard/', views.dashboard, name='dashboard'),  # 선생님 대시보드
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),  # 학생 대시보드

    path('create-task/', views.create_task, name='create_task'),
    path('view-tasks/', views.view_tasks, name='view_tasks'),  # 작업 보기 URL
    path('mark-complete/<int:task_id>/', views.mark_task_complete, name='mark_task_complete'),  # 작업 완료 URL

    # 인증 관련
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),  # 로그인
    path('register/', views.register, name='register'),  # 회원가입
    path('logout/', auth_views.LogoutView.as_view(next_page='core:home'), name='logout'),  # 로그아웃

    # 리디렉션 뷰
    path('after-login/', views.after_login_view, name='after_login'),  # 로그인 후 리디렉션

    # 선생님 요청뷰
     path('request-teacher/', request_teacher_role, name='request_teacher'),
    
]
