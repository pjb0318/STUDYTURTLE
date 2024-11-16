# core/tests.py

from django.test import TestCase
from django.contrib.auth import get_user_model

class UserRoleTestCase(TestCase):
    
    def setUp(self):
        # 관리자 계정 생성 시, is_staff=True로 설정
        self.admin_user = get_user_model().objects.create_user(
            username='adminuser',
            password='adminpassword',
            role='admin',
            is_staff=True,  # 관리자 권한 부여
        )
        
        # 학생 계정 생성
        self.student_user = get_user_model().objects.create_user(
            username='studentuser',
            password='studentpassword',
            role='student',
        )
    
    def test_admin_user(self):
        # 관리자 계정이 정상적으로 생성되었는지 확인
        admin = get_user_model().objects.get(username='adminuser')
        self.assertTrue(admin.is_staff)  # 관리자 계정은 is_staff가 True여야 함
        self.assertEqual(admin.role, 'admin')  # role이 'admin'이어야 함
    
    def test_student_user(self):
        # 학생 계정이 정상적으로 생성되었는지 확인
        student = get_user_model().objects.get(username='studentuser')
        self.assertFalse(student.is_staff)  # 학생 계정은 is_staff가 False여야 함
        self.assertEqual(student.role, 'student')  # role이 'student'이어야 함
    
    def test_user_role_display(self):
        # 관리자와 학생을 구분하여 출력되는지 확인
        admin = get_user_model().objects.get(username='adminuser')
        student = get_user_model().objects.get(username='studentuser')

        # 관리자 계정 출력 확인
        self.assertEqual(str(admin), 'adminuser')  # 관리자 계정 이름 출력 확인
        
        # 학생 계정 출력 확인
        self.assertEqual(str(student), 'studentuser')  # 학생 계정 이름 출력 확인
