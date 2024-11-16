from django.urls import path
from core import views  
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),  # 관리자 대시보드 URL
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),  # 학생 대시보드
    path('create-task/', views.create_task, name='create_task'),  # 작업 추가
    path('mark-complete/<int:task_id>/', views.mark_task_complete, name='mark_task_complete'),  # 작업 완료
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),  # 로그인
    path('register/', views.register, name='register'),  # 회원가입
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),  # 로그아웃 후 홈으로 이동
    path('', views.home, name='home'),  # 홈 페이지 (마지막에 배치)
    path('admin/', admin.site.urls),  # Django 관리자 페이지
    path('', include('core.urls')),  # core 앱의 URL 포함
]
