from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from .models import User, Task, TaskCompletion, Group
from django.shortcuts import render


class ResetPasswordForm(forms.Form):
    """
    비밀번호 초기화를 위한 폼
    """
    new_password = forms.CharField(widget=forms.PasswordInput, label="새 비밀번호")


class CustomUserAdmin(BaseUserAdmin):
    """
    사용자 관리를 위한 커스텀 관리자
    """
    # 사용자 목록에서 표시할 필드
    list_display = ('username', 'email', 'name', 'role', 'student_id', 'is_active', 'is_staff')  # student_id 추가
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'name', 'student_id')  # student_id 검색 가능
    ordering = ('username',)

    # role, name, student_id 필드를 추가하여 수정 가능하도록 설정
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('name', 'student_id', 'role')}),  # name 및 student_id 추가
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # 관리자에서 사용자 추가 시 필요한 필드 정의
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'name', 'student_id', 'role'),
        }),
    )

    actions = ['reset_password']  # 사용자 정의 액션 추가

    @admin.action(description="사용자 비밀번호 초기화")
    def reset_password(self, request, queryset):
        """
        선택한 사용자들의 비밀번호를 초기화하는 액션
        """
        if 'apply' in request.POST:
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password']
                for user in queryset:
                    user.set_password(new_password)  # 비밀번호 암호화 및 저장
                    user.save()
                self.message_user(request, "선택한 사용자들의 비밀번호가 초기화되었습니다.")
                return
        else:
            form = ResetPasswordForm()

        return render(request, 'admin/reset_password.html', {
            'form': form,
            'users': queryset,
        })


# 사용자 관리 모델 등록
admin.site.register(User, CustomUserAdmin)


# 그룹 관리
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Admin 목록에서 표시할 필드
    search_fields = ('name',)  # 검색 가능 필드


# 과제 관리
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'group', 'assigned_by', 'due_date', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('group', 'assigned_by', 'due_date')


# 과제 완료 관리
@admin.register(TaskCompletion)
class TaskCompletionAdmin(admin.ModelAdmin):
    list_display = ('task', 'student', 'status', 'updated_at')
    search_fields = ('task__title', 'student__username')
    list_filter = ('status',)
