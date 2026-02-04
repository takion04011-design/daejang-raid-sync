# 🤖 GitHub Actions 자동 동기화

## 📋 개요

GitHub Actions를 통해 아이온2tool API에서 길드 멤버를 자동으로 수집하고 **DB에 직접 동기화**합니다.

---

## 🎯 주요 기능

### ✅ 완전 자동화
- 매일 자정(UTC) = 한국 시간 오전 9시 자동 실행
- 수동 실행도 가능 (Actions 탭에서)

### ✅ DB 직접 동기화 ⭐
- 아이온2tool API → **DB 직접 업데이트**
- 홈페이지 접속 불필요
- 클릭 불필요
- **수동 작업 0개**

### ✅ 실시간 공유
- 모든 사용자가 즉시 최신 데이터 확인
- 페이지 새로고침만 하면 OK

---

## 📁 파일 구조

```
프로젝트/
├── .github/
│   └── workflows/
│       └── sync-members.yml       # GitHub Actions 워크플로우
├── collect_region.py               # 아이온2tool API 호출
├── sync_to_db.py                   # DB 동기화 스크립트 ⭐
├── test_local.py                   # 로컬 테스트
├── region_members.json             # 멤버 데이터 (JSON)
├── GITHUB_TO_DB_GUIDE.md           # 설정 가이드 (필독!)
└── DB_SYNC_COMPLETE.md             # 완료 보고서
```

---

## 🚀 빠른 시작

### 1️⃣ GitHub 레포지토리 생성
```
https://github.com/new
```

### 2️⃣ 파일 업로드
위의 모든 파일을 레포지토리에 업로드

### 3️⃣ Secrets 설정
```
Settings → Secrets and variables → Actions
New repository secret:
- Name: AION_COOKIE
- Value: <your_aion2tool_cookie>
```

### 4️⃣ API URL 설정
`sync_to_db.py` 11번 줄 수정:
```python
API_BASE_URL = "https://YOUR-SITE.pages.dev/tables"
```

### 5️⃣ 테스트 실행
```
Actions → Sync Guild Members → Run workflow
```

---

## 🔄 작동 원리

```
GitHub Actions (매일 자동)
    ↓
1. collect_region.py 실행
   - 아이온2tool API에서 멤버 수집
   - region_members.json 저장
    ↓
2. sync_to_db.py 실행 ⭐
   - DB의 기존 멤버 삭제
   - 새 멤버 추가
   - ✅ DB 동기화 완료!
    ↓
3. Git Commit & Push
   - region_members.json 커밋
   - Cloudflare Pages 자동 배포
    ↓
✅ 모든 사용자가 최신 데이터 확인 가능!
```

---

## 📖 상세 가이드

자세한 설정 방법은 **[GITHUB_TO_DB_GUIDE.md](GITHUB_TO_DB_GUIDE.md)** 참고

---

## 🧪 로컬 테스트

```bash
# 환경변수 설정
export AION_COOKIE="your_cookie_here"

# 테스트 실행
python test_local.py
```

---

## 📊 실행 결과 예시

```
🔄 길드 멤버 DB 동기화 시작
============================================================
✅ region_members.json에서 54명 데이터 로드
📡 DB에서 길드 멤버 조회 중...
✅ DB에서 51명 조회 완료

🗑️ 기존 멤버 51명 삭제 중...
✅ 51명 삭제 완료

➕ 새 멤버 54명 추가 중...
  [1/54] ✅ 록커 (수호성) - 3322
  [2/54] ✅ 상어 (검성) - 3353
  ...
  [54/54] ✅ 새멤버 (검성) - 2500

============================================================
📊 동기화 결과:
  ✅ 추가 성공: 54명
  ❌ 추가 실패: 0명
  📝 총 처리: 54명
============================================================

🎉 DB 동기화 완료!
모든 사용자가 최신 54명의 길드 멤버를 확인할 수 있습니다.
```

---

## 🐛 문제 해결

### ❌ "API 요청 실패: 403"
→ 쿠키 만료, GitHub Secrets 업데이트

### ❌ "DB 조회 실패: 404"
→ `API_BASE_URL` 확인

### ❌ "추가 실패: 500"
→ DB 스키마 확인

자세한 내용은 **[GITHUB_TO_DB_GUIDE.md](GITHUB_TO_DB_GUIDE.md#-문제-해결)** 참고

---

## 🎉 완료!

이제 GitHub Actions가 매일 자동으로:
- ✅ 멤버 수집
- ✅ DB 동기화
- ✅ 모든 사용자 공유

**수동 작업이 완전히 사라졌습니다!** 🚀

---

**버전**: DB 직접 동기화 v1.0  
**날짜**: 2026-02-04
