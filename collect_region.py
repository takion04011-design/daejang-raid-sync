import requests
import json
import time
import os

# ==========================
# GitHub Actions 환경 설정
# ==========================

DOMAIN = "https://aion2tool.com"
SERVER = "아스펠"
GUILD = "대장"

# GitHub Actions에서 환경변수로 쿠키 가져오기
# 로컬 테스트 시에는 직접 입력
COOKIE = os.getenv('AION_COOKIE', '')

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://aion2tool.com/",
    "Cookie": COOKIE
}

# ==========================
# 실행 코드
# ==========================

def fetch_guild_members():
    """아이온2tool API에서 길드 멤버 정보 가져오기"""
    try:
        print(f"🔍 서버: {SERVER}, 길드: {GUILD}")
        
        # API 엔드포인트 (실제 collect_region.py 참고)
        url = f"{DOMAIN}/api/region/guild"
        params = {
            "server": SERVER,
            "guild": GUILD
        }
        
        print(f"📡 API 요청 중: {url}")
        response = requests.get(url, headers=HEADERS, params=params, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ API 요청 실패: {response.status_code}")
            print(f"응답: {response.text}")
            return None
        
        data = response.json()
        
        if not data or 'members' not in data:
            print("❌ 멤버 데이터가 없습니다.")
            return None
        
        members = data['members']
        print(f"✅ {len(members)}명의 멤버 정보 가져오기 성공!")
        
        return members
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return None

def save_to_json(members, filename='region_members.json'):
    """멤버 데이터를 JSON 파일로 저장"""
    try:
        # 전투력 순으로 정렬
        members_sorted = sorted(
            members, 
            key=lambda x: x.get('combat_power', 0), 
            reverse=True
        )
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(members_sorted, f, ensure_ascii=False, indent=2)
        
        print(f"✅ {filename} 파일에 {len(members_sorted)}명의 데이터 저장 완료!")
        return True
        
    except Exception as e:
        print(f"❌ 파일 저장 실패: {e}")
        return False

def main():
    """메인 실행 함수"""
    print("=" * 50)
    print("🚀 길드 멤버 데이터 동기화 시작")
    print("=" * 50)
    
    # 1. 멤버 데이터 가져오기
    members = fetch_guild_members()
    
    if not members:
        print("❌ 멤버 데이터를 가져올 수 없습니다.")
        exit(1)
    
    # 2. JSON 파일로 저장
    if save_to_json(members):
        print("=" * 50)
        print("✅ 동기화 완료!")
        print("=" * 50)
        
        # 상위 5명 출력
        print("\n📊 전투력 Top 5:")
        for i, member in enumerate(members[:5], 1):
            print(f"  {i}. {member['nickname']} ({member['job']}) - {member['combat_power']}")
    else:
        print("❌ 동기화 실패!")
        exit(1)

if __name__ == "__main__":
    main()
