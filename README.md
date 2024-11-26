### **README for StudyTurtle**

---

## **StudyTurtle**

지원 예정 기능들입니다. 아직 만드는 중이에요~

StudyTurtle은 그룹 기반 학습 관리를 목적으로 설계된 웹 애플리케이션입니다. 학생, 선생님, 관리자를 위한 다양한 기능을 제공하여 효율적인 학습 관리와 협업을 지원합니다.

---

### **Features**

#### **1. 사용자 역할**
- **관리자 (Admin):** 사용자와 그룹을 관리하며, 선생님 계정을 생성할 수 있습니다.
- **선생님 (Teacher):** 그룹을 생성하고 학생을 추가하며, 과제와 학습 자료를 관리합니다.
- **학생 (Student):** 그룹별로 과제를 확인하고 학습 진행 상태를 업데이트하며, 문의를 보낼 수 있습니다.

#### **2. 주요 기능**
- **사용자 관리:**
  - 회원가입 시 기본적으로 `student` 역할이 부여됩니다.
  - 관리자 페이지를 통해 `admin` 및 `teacher` 역할 변경 가능.

- **그룹 관리:**
  - 선생님은 그룹을 생성하고 학생을 추가할 수 있습니다.
  - 그룹 삭제 시 관련된 모든 학생과의 연결도 제거됩니다.

- **과제 관리:**
  - 선생님은 특정 그룹에 과제를 생성, 수정, 삭제할 수 있습니다.
  - 학생은 자신이 속한 그룹의 과제를 확인하고 완료 상태를 업데이트할 수 있습니다.

- **문의 관리:**
  - 학생은 문의를 보낼 수 있으며, 문의는 그룹별로 관리됩니다.
  - 관리자는 문의 상태를 변경하고 답변을 제공합니다.

- **알림 기능:**
  - 과제 생성, 수정, 삭제 시 관련된 학생들에게 알림이 전송됩니다.
  - 알림은 학생 대시보드에 표시됩니다.

- **학습 자료 업로드:**
  - 선생님은 그룹별 학습 자료를 업로드할 수 있습니다.
  - 학생은 자료를 다운로드하여 학습에 활용합니다.

- **학습 일정 관리:**
  - 그룹별 학습 일정을 생성하고 달력 형태로 표시합니다.

- **리워드 시스템:**
  - 과제 완료 및 활동 참여 시 학생에게 포인트가 지급됩니다.

- **설문조사 기능:**
  - 과제 및 스터디 전체 만족도 조사를 통해 피드백을 수집합니다.

- **다크 모드 지원:**
  - 사용자 선택에 따라 라이트/다크 모드 전환 가능.

---

### **Technology Stack**
- **Backend:** Python (Django Framework)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite (개발 중), MySQL (배포 계획)
- **API:** Naver Clova API (문의 내용 감정 분석)

---

### **Installation**

1. **Clone the repository**:
   ```bash
   git clone https://github.com/pjb0318/StudyTurtle.git
   cd StudyTurtle
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv env
   source env/bin/activate   # (Linux/Mac)
   env\Scripts\activate      # (Windows)
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the application**:
   Open a browser and navigate to `http://127.0.0.1:8000`.

---

### **Usage**

#### **Admin**
- 로그인 후 관리자 대시보드에서 사용자 및 그룹을 관리.
- 선생님 계정 생성, 그룹 관리 기능 제공.

#### **Teacher**
- 그룹 생성, 학생 추가, 과제 관리, 학습 자료 업로드.
- 학생 대시보드에서 과제 상태를 확인.

#### **Student**
- 그룹별 과제 확인, 완료 상태 업데이트.
- 문의 기능을 통해 관리자와 소통.
- 학습 자료 다운로드 및 일정 확인.

---

### **Development Goals**
- 실제 동아리 학습 관리에 사용 가능하도록 기능 확장.
- 향후 Java와 JavaScript를 활용하여 프로젝트 확장.
- 프로토타입 완성 후 전역 후 배포 및 서비스화.

---

### **Contributors**
- **Main Developer:** pjb0318


---

### **License**
This project is licensed under the MIT License.