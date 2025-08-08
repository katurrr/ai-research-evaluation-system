# AI Research-Evaluation 피드백 시스템

두 개의 AI 에이전트(리서치 에이전트, 평가 에이전트)가 협업하여 고품질 리서치를 수행하는 시스템입니다.

## 🎯 시스템 개요

- **리서치 에이전트**: 질문에 대해 깊이 있는 리서치 수행
- **평가 에이전트**: 리서치 품질 평가 및 개선 피드백 제공  
- **피드백 루프**: 목표 품질(7/10점) 달성까지 반복 개선
- **최대 반복**: 5회 제한으로 무한 루프 방지

## 📁 프로젝트 구조

```
research-system/
├── src/                    # 소스코드 디렉토리
│   ├── config.py          # 설정 및 프롬프트 관리
│   ├── research_agent.py  # 리서치 에이전트
│   └── evaluation_agent.py # 평가 에이전트
├── venv/                  # 가상환경 (설치 후 생성)
├── .env                   # 환경변수 (설치 후 생성)  
├── .env.example           # 환경변수 예시
├── .gitignore             # Git 무시 파일
├── requirements.txt       # Python 패키지 의존성
├── setup_env.py           # 환경 설정 도우미
├── main.py                # 메인 실행 파일
└── README.md              # 이 파일
```

## 📋 설치 방법

### 방법 1: GitHub에서 클론 (추천)

```bash
# 1. 저장소 클론
git clone https://github.com/your-username/ai-research-system.git
cd ai-research-system

# 2. 자동 환경 설정
python3 setup_env.py

# 3. API 키 및 GitHub 토큰 설정 (.env 파일 편집)
nano .env
# OPENAI_API_KEY와 GITHUB_TOKEN 설정

# 4. 실행
source venv/bin/activate
python3 main.py
```

### 방법 2: 로컬에서 시작

```bash
# 환경 설정 스크립트 실행
python3 setup_env.py
```

이 스크립트가 자동으로 처리하는 것들:
- 가상환경 생성
- 패키지 설치  
- .env 파일 생성

### 2단계: API 키 설정

```bash
# .env 파일 편집
nano .env

# 또는
vi .env
```

`.env` 파일에서 OpenAI API 키를 설정:
```
OPENAI_API_KEY=your_actual_api_key_here
```

### 3단계: 실행

```bash
# 가상환경 활성화
source venv/bin/activate    # Linux/Mac
# 또는
venv\Scripts\activate       # Windows

# 프로그램 실행
python main.py
```

## 🔧 수동 설치 (선택사항)

자동 설정이 작동하지 않을 경우:

```bash
# 1. 가상환경 생성
python -m venv venv

# 2. 가상환경 활성화
source venv/bin/activate    # Linux/Mac
# 또는  
venv\Scripts\activate       # Windows

# 3. 패키지 설치
pip install --upgrade pip
pip install -r requirements.txt

# 4. 환경변수 파일 생성
cp .env.example .env
# .env 파일에서 API 키 설정

# 5. 실행
python main.py
```

## 💡 사용법

### 기본 사용

1. 프로그램 실행 후 질문 입력
2. 리서치 에이전트가 초기 답변 생성
3. 평가 에이전트가 품질 평가 (1-10점)
4. 7점 미만이면 피드백과 함께 재시도
5. 목표 품질 달성 또는 최대 5회 반복 후 종료

### 예시 세션

```
💬 리서치할 질문을 입력하세요: 인공지능의 미래는 어떻게 될까요?

🔍 리서치 시작: 인공지능의 미래는 어떻게 될까요?
===============================================================

📝 반복 #1
----------------------------------------
🤖 리서치 에이전트 작업 중...
⚖️  평가 에이전트 작업 중...
   ⚠️ 점수: 5/10
   🔧 개선점:
      • 더 구체적인 예시 필요
      • 최신 기술 동향 추가 필요

🔄 품질 개선이 필요합니다. 다음 반복을 진행합니다...

📝 반복 #2  
----------------------------------------
🤖 리서치 에이전트 작업 중...
⚖️  평가 에이전트 작업 중...
   ✅ 점수: 8/10
   💪 강점:
      • 포괄적인 분석
      • 구체적인 예시 포함

✅ 목표 품질 달성! (점수: 8/10)
```

## ⚙️ 설정 커스터마이징

`src/config.py`에서 다음 설정들을 변경할 수 있습니다:

```python
# AI 모델 설정
MODEL_NAME = "gpt-4o-mini"  # 사용할 OpenAI 모델

# 품질 기준
QUALITY_THRESHOLD = 7       # 목표 품질 점수 (1-10)

# 반복 제한
MAX_ITERATIONS = 5          # 최대 반복 횟수

# 프롬프트 커스터마이징
RESEARCH_PROMPT = """..."""  # 리서치 에이전트 프롬프트
EVALUATION_PROMPT = """...""" # 평가 에이전트 프롬프트
```

## 🛠️ 개발 정보

### 요구사항

- Python 3.8+
- OpenAI API 키
- 인터넷 연결

### 의존성

- `openai>=1.0.0` - OpenAI API 클라이언트
- `python-dotenv>=1.0.0` - 환경변수 관리

### 아키텍처

```
사용자 질문 → 리서치 에이전트 → 평가 에이전트 → 피드백
                ↑                                    ↓
                ←←←←←←← 품질 미달시 재시도 ←←←←←←←←
```

## 🐛 문제 해결

### 자주 발생하는 문제

1. **API 키 오류**
   ```
   ❌ 오류: OPENAI_API_KEY가 설정되지 않았습니다.
   ```
   → `.env` 파일에서 API 키 확인

2. **모듈 import 오류**  
   ```
   ModuleNotFoundError: No module named 'openai'
   ```
   → 가상환경 활성화 확인 및 `pip install -r requirements.txt`

3. **권한 오류 (Linux/Mac)**
   ```
   Permission denied
   ```
   → `chmod +x setup_env.py`

### 디버깅

에러 발생시 다음을 확인:
- 가상환경이 활성화되었는지 (`venv` 활성화 표시)
- API 키가 올바르게 설정되었는지  
- 인터넷 연결 상태
- Python 버전 (3.8 이상)

## 🔮 향후 계획

- [ ] 웹 인터페이스 추가
- [ ] 리서치 결과 저장/불러오기 기능
- [ ] 다양한 AI 모델 지원 (Anthropic, Google 등)
- [ ] 평가 메트릭 시각화
- [ ] 배치 처리 모드

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🌍 GitHub 저장소 관리

### GitHub에 업로드하기

```bash
# 1. GitHub에서 새 저장소 생성 (ai-research-system)

# 2. GitHub 토큰을 .env에 설정 (위에서 생성한 토큰)
nano .env
# GITHUB_TOKEN=ghp_your_actual_token_here

# 3. 로컬 저장소와 연결
git remote add origin https://github.com/katurrr/ai-research-system.git

# 4. 파일 추가 및 커밋
git add .
git commit -m "Initial commit: AI Research-Evaluation system"

# 5. GitHub에 푸시 (Username: katurrr, Password: 토큰입력)
git push -u origin main
```

**GitHub 토큰 생성:**
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. "Generate new token" → Note: "ai-research-system" → Expiration: 90 days
3. 권한: ✅ **repo** (전체 저장소 권한)
4. Generate token → 토큰 복사 → `.env`에 입력

### 다른 컴퓨터에서 작업하기

```bash
# 1. 저장소 클론
git clone https://github.com/your-username/ai-research-system.git
cd ai-research-system

# 2. 환경 설정
python3 setup_env.py

# 3. API 키 설정
cp .env.example .env
nano .env  # API 키 입력

# 4. 사용 시작
source venv/bin/activate
python3 main.py
```

### 변경사항 동기화

```bash
# 작업 전 최신 버전으로 업데이트
git pull origin main

# 작업 후 변경사항 저장
git add .
git commit -m "작업 내용 설명"
git push origin main
```

### 주의사항

- **절대 .env 파일을 Git에 올리지 마세요** (API 키 유출 위험)
- **venv/ 폴더도 Git에서 제외됩니다** (각 컴퓨터에서 개별 생성)
- **각 컴퓨터에서 개별적으로 API 키 설정 필요**

## 🤝 기여

버그 리포트나 기능 제안은 언제든 환영합니다!

### 기여 방법

1. Fork 생성
2. Feature 브랜치 생성 (`git checkout -b feature/amazing-feature`)
3. 변경사항 커밋 (`git commit -m 'Add amazing feature'`)
4. 브랜치에 푸시 (`git push origin feature/amazing-feature`)
5. Pull Request 생성