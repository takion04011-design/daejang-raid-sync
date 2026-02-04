# 🤖 GitHub Actions → DB 직접 동기화 가이드

## 📋 목차
- [개요](#개요)
- [작동 원리](#작동-원리)
- [설정 방법](#설정-방법)
- [파일 구조](#파일-구조)
- [테스트 방법](#테스트-방법)
- [문제 해결](#문제-해결)

---

## 🎯 개요

GitHub Actions를 통해 **아이온2tool API → DB**로 길드 멤버를 자동 동기화합니다.

### ✨ 주요 장점
- ✅ **완전 자동화**: 매일 자동으로 멤버 데이터 업데이트
- ✅ **수동 작업 불필요**: 홈페이지 접속/클릭 없이 자동 실행
- ✅ **실시간 공유**: 모든 사용자가 즉시 최신 데이터 확인
- ✅ **무료**: GitHub Actions 무료 티어로 충분

---

## 🔄 작동 원리

```
┌─────────────────────────────────────────────────────────────┐
│                   GitHub Actions (매일 자동)                 │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  1. collect_region.py 실행                                   │
│     ↓                                                        │
│     아이온2tool API에서 길드 멤버 수집                        │
│     ↓                                                        │
│     region_members.json 파일에 저장                           │
│                                                               │
│  2. sync_to_db.py 실행                                       │
│     ↓                                                        │
│     DB의 기존 멤버 모두 삭제                                  │
│     ↓                                                        │
│     region_members.json의 멤버를 DB에 추가                    │
│     ↓                                                        │
│     ✅ DB 동기화 완료!                                        │
│                                                               │
│  3. Git Commit & Push                                        │
│     ↓                                                        │
│     region_members.json 파일 커밋                             │
│     ↓                                                        │
│     Cloudflare Pages 자동 배포                                │
│                                                               │
└─────────────────────────────────────────────────────────────┘

결과: 모든 사용자가 최신 멤버 데이터 확인 가능!
```

---

## ⚙️ 설정 방법

### 1️⃣ GitHub 레포지토리 생성

1. https://github.com/new 접속
2. Repository name: `daejang-raid-sync` (원하는 이름)
3. **Public** 선택
4. `README.md` 체크
5. **Create repository** 클릭

---

### 2️⃣ 파일 업로드

다음 파일들을 레포지토리에 업로드:

```
daejang-raid-sync/
├── .github/
│   └── workflows/
│       └── sync-members.yml       # GitHub Actions 워크플로우
├── collect_region.py               # 아이온2tool API 호출
├── sync_to_db.py                   # DB 동기화 스크립트
└── region_members.json             # 초기 파일 (빈 배열 [])
```

**region_members.json 초기 내용:**
```json
[]
```

---

### 3️⃣ GitHub Secrets 설정

#### 필수: AION_COOKIE

1. 레포지토리 → **Settings** → **Secrets and variables** → **Actions**
2. **New repository secret** 클릭
3. **Name**: `AION_COOKIE`
4. **Value**: 여러분의 아이온2tool 쿠키 값
5. **Add secret** 클릭

**쿠키 가져오는 방법:**
1. Chrome에서 https://aion2tool.com 접속 및 로그인
2. F12 (개발자 도구) → **Application** 탭 → **Cookies**
3. 쿠키 값 복사 (전체 문자열)

예시:
```
sessionid=abc123...; csrftoken=xyz789...
```

---

### 4️⃣ API_BASE_URL 설정

`sync_to_db.py` 파일의 **11번 줄** 수정:

**현재 (수정 전):**
```python
API_BASE_URL = "https://daejang-raid.pages.dev/tables"
```

**여러분의 URL로 변경:**
```python
# 운영 서버
API_BASE_URL = "https://YOUR-SITE.pages.dev/tables"

# 또는 Preview URL
API_BASE_URL = "https://YOUR-PREVIEW.genspark.ai/tables"
```

---

## 📁 파일 구조

### 1. `.github/workflows/sync-members.yml`
- GitHub Actions 워크플로우
- 매일 자정(UTC) = 한국 시간 오전 9시 실행
- 수동 실행도 가능

### 2. `collect_region.py`
- 아이온2tool API에서 길드 멤버 가져오기
- `region_members.json` 파일에 저장

### 3. `sync_to_db.py` ⭐ **NEW!**
- `region_members.json` 데이터를 DB에 동기화
- 기존 멤버 삭제 → 새 멤버 추가
- RESTful Table API 사용

### 4. `region_members.json`
- 길드 멤버 데이터 (JSON 형식)
- GitHub Actions가 자동 업데이트

---

## 🧪 테스트 방법

### 1️⃣ 수동 실행 (권장)

1. 레포지토리 → **Actions** 탭
2. **Sync Guild Members** 워크플로우 선택
3. **Run workflow** → **Run workflow** 클릭
4. 실행 결과 확인:
   - ✅ 초록색: 성공
   - ❌ 빨간색: 실패 (로그 확인)

### 2️⃣ 로그 확인

워크플로우 실행 후:
1. 실행 항목 클릭
2. **sync** job 클릭
3. 각 단계별 로그 확인:
   - **Fetch guild members from API**: 멤버 수집 로그
   - **Sync members to database**: DB 동기화 로그
   - **Commit and push**: Git 커밋 로그

**성공 로그 예시:**
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

### 3️⃣ 웹사이트에서 확인

1. https://daejang-raid.pages.dev/ 접속
2. **데이터 관리** 탭 클릭
3. 비밀번호 입력: `Bluecoat123$`
4. **⬇️ DB → 로컬 다운로드** 클릭
5. 멤버 수 확인 (54명이어야 함)

---

## 🐛 문제 해결

### ❌ 문제 1: "API 요청 실패: 403"
**원인**: 쿠키가 만료되었거나 잘못됨  
**해결**:
1. 아이온2tool에 다시 로그인
2. 새 쿠키 복사
3. GitHub Secrets에서 `AION_COOKIE` 업데이트

---

### ❌ 문제 2: "DB 조회 실패: 404"
**원인**: API_BASE_URL이 잘못됨  
**해결**:
1. `sync_to_db.py` 11번 줄 확인
2. 올바른 URL로 수정:
   ```python
   API_BASE_URL = "https://YOUR-SITE.pages.dev/tables"
   ```
3. Git commit & push

---

### ❌ 문제 3: "추가 실패: 500 Internal Server Error"
**원인**: DB 스키마 불일치 또는 서버 오류  
**해결**:
1. DB 스키마 확인:
   ```javascript
   // guild_members 테이블 필드
   {
     "nickname": "text",
     "job": "text",
     "power": "number",
     "server": "text"
   }
   ```
2. 필드명이 정확히 일치하는지 확인

---

### ❌ 문제 4: "기존 멤버 삭제 실패"
**원인**: Record ID를 찾을 수 없음  
**해결**:
1. `sync_to_db.py` 71번 줄 확인:
   ```python
   record_id = member.get('gs_record_id') or member.get('id')
   ```
2. DB 응답에 `gs_record_id` 또는 `id` 필드가 있는지 확인

---

## 📊 자동 실행 스케줄

### 기본 스케줄
```yaml
schedule:
  - cron: '0 0 * * *'  # 매일 자정(UTC) = 한국 오전 9시
```

### 스케줄 변경하기

`sync-members.yml` 5번 줄 수정:

**매일 자정(KST)**:
```yaml
- cron: '0 15 * * *'  # UTC 15:00 = KST 00:00
```

**매일 오전 6시(KST)**:
```yaml
- cron: '0 21 * * *'  # UTC 21:00 = KST 06:00
```

**주중만 오전 9시(KST)**:
```yaml
- cron: '0 0 * * 1-5'  # 월~금만 실행
```

---

## 🎉 완료!

이제 GitHub Actions가 매일 자동으로:
1. 아이온2tool에서 멤버 수집
2. DB에 직접 동기화
3. 모든 사용자가 최신 데이터 확인

**수동 작업이 완전히 사라졌습니다!** 🚀

---

## 📚 추가 자료

- [GitHub Actions 공식 문서](https://docs.github.com/actions)
- [RESTful Table API 문서](../README.md#-db-동기화-api)
- [문제 해결 가이드](../README.md#-문제-해결)

---

**작성일**: 2026-02-04  
**버전**: DB 직접 동기화 v1.0
