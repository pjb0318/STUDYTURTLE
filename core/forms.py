from django import forms
from .models import Task
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from core.models import Group, User



User = get_user_model()  # 사용자 정의 모델 가져오기
from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models import User


class UserRegistrationForm(UserCreationForm):
    name = forms.CharField(
        label="이름",
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': '이름을 입력하세요.',
            'max_length': '이름은 최대 50자까지 입력 가능합니다.',
        },
    )
    student_id = forms.CharField(
        label="학번",
        max_length=8,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': '학번을 입력하세요.',
            'max_length': '학번은 최대 8자리여야 합니다.',
        },
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'student_id', 'password1', 'password2']
        labels = {
            'username': '아이디',
            'email': '이메일 주소',
            'password1': '비밀번호',
            'password2': '비밀번호 확인',
        }
        error_messages = {
            'username': {
                'required': '아이디를 입력하세요.',
                'max_length': '아이디는 최대 150자까지 입력 가능합니다.',
            },
            'email': {
                'required': '이메일 주소를 입력하세요.',
                'invalid': '올바른 이메일 주소를 입력하세요.',
            },
            'password1': {
                'required': '비밀번호를 입력하세요.',
            },
            'password2': {
                'required': '비밀번호 확인란을 입력하세요.',
            },
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("이미 등록된 이메일 주소입니다.")
        return email

    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        if len(student_id) != 8:
            raise forms.ValidationError("학번은 정확히 8자리여야 합니다.")
        if not student_id.isdigit():
            raise forms.ValidationError("학번은 숫자로만 이루어져야 합니다.")
        if User.objects.filter(student_id=student_id).exists():
            raise forms.ValidationError("이미 등록된 학번입니다.")
        return student_id

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        if len(password1) < 8:
            raise forms.ValidationError("비밀번호는 최소 8자 이상이어야 합니다.")
        if password1.isdigit():
            raise forms.ValidationError("비밀번호는 숫자만으로 구성될 수 없습니다.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.name = self.cleaned_data['name']
        user.student_id = self.cleaned_data['student_id']
        user.role = 'student'  # 기본 역할 설정
        if commit:
            user.save()
        return user



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
        fields = ['title', 'description', 'due_date', 'group']  # 'assigned_by'는 폼에 포함되지 않음
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '과제 제목 입력'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': '과제 설명 입력'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'group': forms.Select(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        # 상위 클래스의 save() 호출 후 커밋 없이 Task 객체를 반환
        task = super().save(commit=False)
        
        # 'assigned_by' 필드를 폼 초기 데이터에서 가져와 설정
        if 'assigned_by' in self.initial:
            task.assigned_by = self.initial['assigned_by']  # 초기 데이터에서 설정된 assigned_by 사용
        else:
            # assigned_by가 초기 데이터에 없으면 오류 발생
            raise ValueError("'assigned_by' 필드는 폼의 초기 데이터에 반드시 포함되어야 합니다.")

        # 커밋 플래그에 따라 데이터베이스에 저장
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