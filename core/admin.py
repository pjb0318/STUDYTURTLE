from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from .models import User, Task, TaskCompletion
from django.shortcuts import render
from core.models import Group

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
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('username',)
    
    # role 필드를 추가하여 수정 가능하도록 설정
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('role',)}),  # role 필드 추가
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
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


# 기존 모델 등록
admin.site.register(User, CustomUserAdmin)  # 사용자 모델
admin.site.register(Task)  # 작업 모델
admin.site.register(TaskCompletion)  # 작업 완료 모델



@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Admin 목록에서 표시할 필드
    search_fields = ('name',)  # 검색 가능 필드
