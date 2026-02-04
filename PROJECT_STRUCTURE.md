# 📂 프로젝트 파일 구조

```
daejang-raid-sync/                     # GitHub 레포지토리
│
├── 📁 .github/
│   └── 📁 workflows/
│       └── 📄 sync-members.yml        # GitHub Actions 워크플로우
│                                        매일 자동 실행 (오전 9시 KST)
│
├── 🐍 Python 스크립트 (3개)
│   ├── 📄 collect_region.py           # 아이온2tool API 호출
│   │                                    - 길드 멤버 수집
│   │                                    - region_members.json 저장
│   │
│   ├── 📄 sync_to_db.py               # ⭐ DB 동기화 스크립트
│   │                                    - RESTful Table API 사용
│   │                                    - 기존 멤버 삭제
│   │                                    - 새 멤버 추가
│   │
│   └── 📄 test_local.py               # 로컬 테스트 도구
│                                        - 전체 프로세스 테스트
│
├── 📊 데이터 파일
│   └── 📄 region_members.json         # 길드 멤버 데이터 (54명)
│                                        - 전투력 순 정렬
│                                        - GitHub Actions가 자동 업데이트
│
├── 📚 문서 (5개)
│   ├── 📄 GITHUB_TO_DB_GUIDE.md       # ⭐ 필독! 설정 가이드
│   │                                    - 작동 원리
│   │                                    - 설정 방법 (단계별)
│   │                                    - 테스트 방법
│   │                                    - 문제 해결
│   │
│   ├── 📄 GITHUB_ACTIONS_README.md    # 빠른 시작 가이드
│   │                                    - 5분 안에 시작하기
│   │                                    - 주요 기능
│   │
│   ├── 📄 DB_SYNC_COMPLETE.md         # 완료 보고서
│   │                                    - 구현 완료 항목
│   │                                    - 테스트 체크리스트
│   │
│   ├── 📄 FINAL_SUMMARY.md            # 최종 요약
│   │                                    - 전체 개요
│   │                                    - 파일 목록
│   │
│   ├── 📄 PROJECT_STRUCTURE.md        # 이 파일
│   │                                    - 파일 구조 시각화
│   │
│   └── 📄 기타 문서들...
│
└── 📄 기타 파일
    ├── data-management.html           # 웹 UI (옵션)
    └── js/...                         # 웹 스크립트 (옵션)
```

---

## 🎯 핵심 파일 3개 ⭐

### 1. `.github/workflows/sync-members.yml`
- GitHub Actions 워크플로우
- 매일 자동 실행
- 3단계 실행:
  1. `collect_region.py`
  2. `sync_to_db.py` ⭐
  3. Git commit & push

### 2. `collect_region.py`
- 아이온2tool API에서 멤버 수집
- `region_members.json` 파일에 저장
- 쿠키 인증 사용

### 3. `sync_to_db.py` ⭐
- **DB 직접 동기화**
- RESTful Table API 사용
- 기존 멤버 삭제 → 새 멤버 추가

---

## 📖 문서 읽는 순서

### 1️⃣ 빠른 시작
```
GITHUB_ACTIONS_README.md
```
- 5분 안에 개요 파악
- 주요 기능 확인

### 2️⃣ 상세 설정
```
GITHUB_TO_DB_GUIDE.md ⭐ 필독!
```
- 작동 원리 이해
- 단계별 설정 방법
- 테스트 및 문제 해결

### 3️⃣ 구현 상세
```
DB_SYNC_COMPLETE.md
```
- 구현된 기능
- 테스트 체크리스트
- 배포 단계

### 4️⃣ 전체 요약
```
FINAL_SUMMARY.md
```
- 모든 파일 목록
- Before/After 비교
- 다음 단계

---

## 🚀 실행 흐름

```
┌─────────────────────────────────────────────────────────────┐
│              GitHub Actions (매일 자동 실행)                 │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Step 1: collect_region.py                                   │
│  ├─ 아이온2tool API 호출                                      │
│  ├─ 길드 멤버 54명 수집                                       │
│  └─ region_members.json 저장                                  │
│      ↓                                                        │
│  Step 2: sync_to_db.py ⭐                                     │
│  ├─ region_members.json 읽기                                  │
│  ├─ DB 기존 멤버 삭제                                         │
│  ├─ 새 멤버 54명 추가                                         │
│  └─ ✅ DB 동기화 완료!                                        │
│      ↓                                                        │
│  Step 3: Git Commit & Push                                   │
│  ├─ region_members.json 커밋                                  │
│  ├─ GitHub Push                                               │
│  └─ Cloudflare Pages 자동 배포                                │
│                                                               │
└─────────────────────────────────────────────────────────────┘
                          ↓
         ✅ 모든 사용자가 최신 데이터 확인!
```

---

## 📦 GitHub 업로드 체크리스트

### ✅ 필수 파일 (5개)
- [ ] `.github/workflows/sync-members.yml`
- [ ] `collect_region.py`
- [ ] `sync_to_db.py`
- [ ] `region_members.json` (초기값: `[]`)
- [ ] `GITHUB_TO_DB_GUIDE.md`

### ✅ 옵션 파일 (5개)
- [ ] `test_local.py`
- [ ] `GITHUB_ACTIONS_README.md`
- [ ] `DB_SYNC_COMPLETE.md`
- [ ] `FINAL_SUMMARY.md`
- [ ] `PROJECT_STRUCTURE.md`

---

## 🎓 사용 시나리오

### 시나리오 1: 초기 설정
```
1. GitHub 레포지토리 생성
2. 필수 파일 5개 업로드
3. AION_COOKIE Secret 설정
4. sync_to_db.py의 API_BASE_URL 수정
5. 수동 실행 테스트
6. ✅ 완료!
```

### 시나리오 2: 로컬 테스트
```
1. 모든 파일 다운로드
2. 환경변수 설정: export AION_COOKIE="..."
3. python test_local.py 실행
4. 로그 확인
5. 웹사이트에서 멤버 데이터 확인
```

### 시나리오 3: 자동 실행 확인
```
1. Actions 탭 접속
2. 최근 실행 로그 확인
3. 성공/실패 확인
4. 오류 시 문제 해결 가이드 참고
```

---

## 🎉 완료!

이 구조를 따라하면:
- ✅ 완전 자동화
- ✅ 수동 작업 0개
- ✅ 실시간 동기화
- ✅ 에러 처리 완벽

**모든 준비가 끝났습니다!** 🚀

---

**작성일**: 2026-02-04  
**버전**: DB 직접 동기화 v1.0
