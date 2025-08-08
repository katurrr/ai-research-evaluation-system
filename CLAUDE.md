# Claude Code 컨텍스트

## 프로젝트: AI Research-Evaluation 시스템
- **개념**: 두 AI 에이전트(리서치 에이전트 + 평가 에이전트)가 협업하여 고품질 리서치 수행
- **메커니즘**: 목표 품질(7/10점) 달성까지 피드백 루프 반복 (최대 5회)
- **언어**: Python 3.8+, OpenAI API (gpt-4o-mini 모델)
- **특징**: 자동 품질 개선, 구조화된 평가, 실시간 피드백

## 현재 상태 (2025-01-08)
- ✅ **핵심 시스템 구현 완료**: 리서치-평가 루프 정상 작동
- ✅ **가상환경 + 프로젝트 구조화**: src/ 디렉토리 구조 적용
- ✅ **GitHub 연동 완료**: 다중 컴퓨터 환경 지원
- ✅ **UTF-8 인코딩 문제 해결**: API 응답 처리 개선
- ✅ **GitHub CLI 인증**: 브라우저 OAuth 인증 완료
- 🎯 **실용적 사용 가능**: 실제 리서치 작업에 활용 준비됨

## 개발 환경
- **사용자**: katurrr (GitHub ID)
- **이메일**: katurrr@users.noreply.github.com (GitHub noreply)
- **저장소**: https://github.com/katurrr/ai-research-evaluation-system
- **실행 방법**: 
  ```bash
  source venv/bin/activate
  python3 main.py
  ```

## 주요 파일 구조
```
ai-research-evaluation-system/
├── src/
│   ├── config.py          # 프롬프트, 모델 설정 (gpt-4o-mini)
│   ├── research_agent.py  # 리서치 수행 + UTF-8 인코딩 처리
│   └── evaluation_agent.py # 품질 평가 + JSON 파싱
├── main.py               # 메인 실행 루프, 사용자 인터페이스
├── setup_env.py          # 가상환경 자동 설정 (Python 버전 감지)
├── requirements.txt      # openai>=1.0.0, python-dotenv>=1.0.0
├── .env                 # API 키 (OPENAI_API_KEY, GITHUB_TOKEN)
├── .env.example         # 환경변수 템플릿
├── README.md            # 상세 사용 설명서
└── CLAUDE.md            # 이 파일
```

## 핵심 설정 정보
- **AI 모델**: gpt-4o-mini (OpenAI)
- **품질 기준**: 7/10점 (QUALITY_THRESHOLD)
- **최대 반복**: 5회 (MAX_ITERATIONS)
- **평가 기준**: 완전성, 정확성, 깊이, 구조, 실용성
- **온도 설정**: Research(0.7), Evaluation(0.3)

## 중요한 기술적 해결사항
1. **UTF-8 인코딩**: `content.encode('utf-8', 'ignore').decode('utf-8', 'ignore')`로 해결
2. **Python 명령어 호환성**: 시스템별 python/python3 자동 감지
3. **GitHub 인증**: Personal Access Token + GitHub CLI 브라우저 인증
4. **이메일 프라이버시**: GitHub noreply 이메일 사용

## 사용법 요약
1. **환경 설정**: `python3 setup_env.py`
2. **API 키 설정**: `.env` 파일에 OPENAI_API_KEY 입력
3. **실행**: `python3 main.py`
4. **질문 입력**: 시스템이 자동으로 품질 개선 루프 실행

## 성능 특징
- **자동 재시도**: 품질 미달 시 피드백과 함께 개선
- **점수 추적**: 각 반복의 점수 변화 시각적 표시
- **시간 측정**: 전체 리서치 소요 시간 표시
- **강점/개선점 분석**: 구체적인 피드백 제공

## 향후 개선 계획 (우선순위 순)
- [ ] **웹 인터페이스 추가**: Flask/FastAPI 기반 웹UI (2단계 목표)
- [ ] **리서치 결과 저장**: JSON/CSV 형태로 결과 저장 기능
- [ ] **다양한 AI 모델 지원**: Anthropic Claude, Google Gemini 등
- [ ] **배치 처리 모드**: 여러 질문 동시 처리
- [ ] **평가 메트릭 시각화**: 점수 변화 그래프
- [ ] **커스텀 평가 기준**: 사용자 정의 평가 항목

## 알려진 이슈 및 해결상태
- ~~UTF-8 인코딩 오류~~: ✅ 해결됨 (API 응답 처리 개선)
- ~~python/python3 명령어 문제~~: ✅ 해결됨 (자동 감지)
- ~~GitHub 토큰 권한 문제~~: ✅ 해결됨 (브라우저 인증)
- **현재 알려진 이슈**: 없음

## 개발 히스토리
1. **초기 구현**: 기본 리서치-평가 시스템 구축
2. **가상환경 구조화**: src/ 디렉토리 구조 적용, setup_env.py 개발
3. **GitHub 연동**: Git 설정, 원격 저장소 연결
4. **인코딩 문제 해결**: UTF-8 처리 로직 추가
5. **GitHub CLI 통합**: 브라우저 인증, 자동 업로드
6. **문서화 완성**: README.md 상세화, CLAUDE.md 추가

## Claude Code 협업 정보
- **개발 스타일**: 체계적 접근, TodoWrite 활용, 단계별 진행
- **코드 품질**: 에러 핸들링, 사용자 친화적 인터페이스
- **문서화**: 상세한 README, 인라인 주석, 사용 예시
- **Git 관리**: 의미있는 커밋 메시지, .gitignore 적절한 설정

## 다음 세션 시작 가이드
새로운 컴퓨터/세션에서 작업 시:
1. 저장소 클론: `git clone https://github.com/katurrr/ai-research-evaluation-system.git`
2. 환경 설정: `python3 setup_env.py`
3. API 키 설정: `.env` 파일에 OPENAI_API_KEY 입력
4. 현재 상태: 이 CLAUDE.md 파일 참조
5. 테스트 실행: `python3 main.py`로 동작 확인

## 프로젝트 가치
- **교육적**: AI 에이전트 협업 패턴 학습
- **실용적**: 실제 리서치 작업에 활용 가능
- **확장 가능**: 다양한 도메인으로 응용 가능
- **포트폴리오**: GitHub 프로젝트로 활용 가능