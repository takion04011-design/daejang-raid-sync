# 🔄 GitHub 자동 멤버 동기화 시스템

## 📋 개요

GitHub Actions를 사용하여 아이온2tool에서 길드 멤버 정보를 매일 자동으로 수집하고, 웹사이트에서 클릭 한 번으로 최신 데이터를 불러올 수 있습니다.

---

## 🚀 설정 방법

### 1. GitHub 레포지토리 생성

1. GitHub에서 새 레포지토리 생성
2. 다음 파일들을 업로드:
   - `collect_region.py` (멤버 수집 스크립트)
   - `.github/workflows/sync-members.yml` (자동화 워크플로우)
   - `region_members.json` (초기 빈 파일: `[]`)

### 2. GitHub Secrets 설정

1. 레포지토리 → Settings → Secrets and variables → Actions
2. "New repository secret" 클릭
3. 다음 시크릿 추가:

**Name**: `AION_COOKIE`  
**Value**: 아이온2tool 쿠키 전체 문자열

```
_fwb=37dKyWquzKeB4EGIG223Rj.1769061550462; cf_clearance=wdljo1QF3Qh1MXQ2GD5JFjTStQALcwmCtLjcBB9g6b0-1770184562-1.2.1.1-...
```

### 3. GitHub Actions 활성화

1. 레포지토리 → Actions 탭
2. "I understand my workflows, go ahead and enable them" 클릭

### 4. 첫 실행 테스트

1. Actions 탭 → "Sync Guild Members" 워크플로우 선택
2. "Run workflow" 버튼 클릭
3. 실행 결과 확인

---

## 🔄 작동 방식

### 자동 실행
- **매일 자정(UTC)** = 한국 시간 오전 9시
- GitHub Actions가 자동으로 `collect_region.py` 실행
- 멤버 데이터 수집 후 `region_members.json` 업데이트
- 변경사항이 있으면 자동 커밋 & 푸시

### 수동 실행
- Actions 탭에서 언제든지 "Run workflow" 클릭

### 웹사이트에서 사용
1. 데이터 관리 페이지 접속
2. 비밀번호 입력: `Bluecoat123$`
3. **"🔄 GitHub에서 가져오기"** 버튼 클릭
4. 최신 멤버 데이터 자동 로드
5. "💾 로컬 저장" → "⬆️ 로컬 → DB 업로드"

---

## 📁 파일 구조

```
프로젝트/
├── .github/
│   └── workflows/
│       └── sync-members.yml      # GitHub Actions 워크플로우
├── collect_region.py             # 멤버 수집 스크립트
├── region_members.json           # 수집된 멤버 데이터 (자동 생성)
├── js/
│   └── data-management.js        # GitHub 데이터 로드 기능 추가
└── data-management.html          # "GitHub에서 가져오기" 버튼 추가
```

---

## 🔧 collect_region.py 주요 기능

### 환경 변수 사용
```python
# GitHub Actions에서 자동으로 쿠키 주입
COOKIE = os.getenv('AION_COOKIE', '')
```

### 데이터 수집
```python
def fetch_guild_members():
    # 아이온2tool API 호출
    # 길드 멤버 정보 가져오기
```

### JSON 저장
```python
def save_to_json(members):
    # 전투력 순으로 정렬
    # region_members.json 파일 생성
```

---

## 🌐 웹사이트 통합

### data-management.js 추가 기능

```javascript
// GitHub에서 최신 멤버 데이터 가져오기
async function loadFromGitHub() {
    const response = await fetch('/region_members.json');
    const jsonData = await response.json();
    
    // CSV 형식으로 변환
    const csv = jsonData.map(member => {
        return `${member.nickname},${member.job},${member.combat_power}`;
    }).join('\n');
    
    // UI 업데이트
    document.getElementById('data-input').value = csv;
}
```

### HTML 버튼 추가

```html
<button onclick="loadFromGitHub()" class="btn-secondary" 
        style="background-color: #6c5ce7;">
    🔄 GitHub에서 가져오기
</button>
```

---

## 📊 데이터 형식

### region_members.json
```json
[
  {
    "combat_power": 3322,
    "combat_score_max": 77443.0,
    "job": "수호성",
    "nickname": "록커",
    "race": "마족",
    "server": "아스펠"
  },
  ...
]
```

### 웹사이트 CSV 형식 (자동 변환)
```
록커,수호성,3322
상어,검성,3353
고래,궁성,3237
...
```

---

## ⚙️ 고급 설정

### 실행 시간 변경

`.github/workflows/sync-members.yml`에서 cron 수정:

```yaml
schedule:
  # 매일 오전 9시(KST) = 자정(UTC)
  - cron: '0 0 * * *'
  
  # 12시간마다
  # - cron: '0 */12 * * *'
  
  # 매주 월요일 오전 9시
  # - cron: '0 0 * * 1'
```

### API 엔드포인트 수정

`collect_region.py`에서 URL 변경:

```python
url = f"{DOMAIN}/api/region/guild"
params = {
    "server": SERVER,
    "guild": GUILD
}
```

---

## 🐛 문제 해결

### GitHub Actions 실행 실패

1. **쿠키 만료**: GitHub Secrets에서 `AION_COOKIE` 업데이트
2. **API 변경**: `collect_region.py`의 엔드포인트 확인
3. **로그 확인**: Actions 탭 → 실패한 워크플로우 → 로그 확인

### 웹사이트에서 데이터 로드 실패

1. **파일 경로**: `region_members.json`이 루트에 있는지 확인
2. **CORS 문제**: 같은 도메인에서 호스팅되는지 확인
3. **브라우저 콘솔**: F12 → Console에서 에러 확인

### 데이터가 업데이트되지 않음

1. GitHub 레포지토리에서 `region_members.json` 최종 수정 시간 확인
2. 웹사이트 배포 확인 (Cloudflare Pages 자동 배포)
3. 브라우저 캐시 삭제 (Ctrl+Shift+R)

---

## ✅ 장점

| 항목 | 설명 |
|------|------|
| 🤖 **완전 자동화** | 매일 정해진 시간에 자동 실행 |
| 💰 **무료** | GitHub Actions 무료 사용 |
| 🔒 **보안** | 쿠키를 GitHub Secrets에 암호화 저장 |
| 🚀 **간편 사용** | 웹사이트에서 버튼 클릭만으로 최신 데이터 |
| 📊 **이력 관리** | Git으로 데이터 변경 이력 추적 |
| 🔄 **실시간 동기화** | Cloudflare Pages 자동 배포 |

---

## 📝 사용 흐름

1. **GitHub Actions** (자동)
   ```
   매일 오전 9시
   → Python 스크립트 실행
   → 아이온2tool에서 데이터 수집
   → region_members.json 업데이트
   → Git 커밋 & 푸시
   ```

2. **Cloudflare Pages** (자동)
   ```
   Git 푸시 감지
   → 웹사이트 자동 재배포
   → 최신 region_members.json 반영
   ```

3. **관리자** (수동)
   ```
   데이터 관리 페이지 접속
   → "GitHub에서 가져오기" 클릭
   → 최신 데이터 확인
   → "로컬 → DB 업로드"
   → 모든 사용자가 최신 데이터 공유
   ```

---

## 🎯 다음 단계

1. ✅ GitHub 레포지토리 생성
2. ✅ 파일 업로드 (collect_region.py, sync-members.yml)
3. ✅ GitHub Secrets 설정 (AION_COOKIE)
4. ✅ 첫 워크플로우 수동 실행
5. ✅ 웹사이트에 파일 배포 (region_members.json)
6. ✅ 데이터 관리 페이지에서 테스트

---

**작성일**: 2026-02-04  
**버전**: 1.0.0  
**상태**: ✅ 준비 완료
