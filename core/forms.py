from django import forms
from .models import Task
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from core.models import Group, User



User = get_user_model()  # 사용자 정의 모델 가져오기



# 사용자 등록 폼
class UserRegistrationForm(UserCreationForm):
    name = forms.CharField(
        label="이름",
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    student_id = forms.CharField(
        label="학번",
        max_length=8,  # 최대 길이 제한
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'student_id', 'password1', 'password2']
        labels = {
            'username': '사용자 이름',
            'email': '이메일 주소',
            'password1': '비밀번호',
            'password2': '비밀번호 확인',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("이미 등록된 이메일입니다.")
        return email

    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        if len(student_id) != 8:
            raise forms.ValidationError("학번은 8자리여야 합니다.")
        if not student_id.isdigit():
            raise forms.ValidationError("학번은 숫자로만 이루어져야 합니다.")
        if User.objects.filter(student_id=student_id).exists():
            raise forms.ValidationError("이미 등록된 학번입니다.")
        return student_id

    def save(self, commit=True):
        user = super().save(commit=False)
        user.name = self.cleaned_data['name']
        user.student_id = self.cleaned_data['student_id']
        user.role = 'student'  # 기본적으로 학생으로 설정
        if commit:
            user.save()
        return user
    

# TaskForm 정의
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'group']  # assigned_by는 제외
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '과제 제목 입력'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': '과제 설명 입력'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'group': forms.Select(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        task = super().save(commit=False)
        # 'assigned_by' 필드에 현재 사용자 설정
        if 'assigned_by' in self.initial:
            task.assigned_by = self.initial['assigned_by']
        else:
            raise ValueError("The 'assigned_by' field must be set in the form's initial data.")
        if commit:
            task.save()
        return task


# AddStudentToGroupForm 정의
class AddStudentToGroupForm(forms.Form):
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="그룹"
    )
    student = forms.ModelChoiceField(
        queryset=User.objects.filter(role='student'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="학생"
    )

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '그룹 이름'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '그룹 설명'}),
        }



class AddStudentToGroupForm(forms.Form):
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="그룹"
    )
    student = forms.ModelChoiceField(
        queryset=User.objects.filter(role='student'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="학생"
    )