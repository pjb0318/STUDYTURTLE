from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from .models import User, Task, TaskCompletion
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
