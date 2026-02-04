import requests
import json
import time
import os

# ==========================
# DB API 설정
# ==========================

# 여러분의 Table API 엔드포인트
API_BASE_URL = "https://daejang-raid.pages.dev/tables"
# 또는 Preview URL: https://your-preview.genspark.ai/tables

# ==========================
# DB API 함수들
# ==========================

def fetch_all_members():
    """DB에서 모든 길드 멤버 가져오기"""
    try:
        url = f"{API_BASE_URL}/guild_members"
        params = {"limit": 1000}
        
        print(f"📡 DB에서 길드 멤버 조회 중...")
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            members = data.get('data', [])
            print(f"✅ DB에서 {len(members)}명 조회 완료")
            return members
        else:
            print(f"⚠️ DB 조회 실패: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ DB 조회 오류: {e}")
        return []

def delete_member(record_id):
    """DB에서 멤버 삭제 (Soft delete)"""
    try:
        url = f"{API_BASE_URL}/guild_members/{record_id}"
        response = requests.delete(url, timeout=30)
        
        if response.status_code == 204:
            return True
        else:
            print(f"⚠️ 삭제 실패 (ID: {record_id}): {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 삭제 오류 (ID: {record_id}): {e}")
        return False

def create_member(member_data):
    """DB에 새 멤버 추가"""
    try:
        url = f"{API_BASE_URL}/guild_members"
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(url, json=member_data, headers=headers, timeout=30)
        
        if response.status_code == 201:
            return True
        else:
            print(f"⚠️ 추가 실패 ({member_data['nickname']}): {response.status_code}")
            print(f"응답: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 추가 오류 ({member_data.get('nickname', 'Unknown')}): {e}")
        return False

# ==========================
# 동기화 로직
# ==========================

def sync_members_to_db(json_file='region_members.json'):
    """
    region_members.json 파일의 데이터를 DB에 동기화
    
    전략:
    1. DB의 모든 멤버 삭제
    2. JSON 파일의 멤버를 DB에 추가
    """
    
    print("=" * 60)
    print("🔄 길드 멤버 DB 동기화 시작")
    print("=" * 60)
    
    # 1. JSON 파일 읽기
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            new_members = json.load(f)
        print(f"✅ {json_file}에서 {len(new_members)}명 데이터 로드")
    except Exception as e:
        print(f"❌ JSON 파일 읽기 실패: {e}")
        return False
    
    if not new_members:
        print("⚠️ 동기화할 멤버가 없습니다.")
        return False
    
    # 2. DB의 기존 멤버 조회
    existing_members = fetch_all_members()
    
    # 3. 기존 멤버 모두 삭제
    if existing_members:
        print(f"\n🗑️ 기존 멤버 {len(existing_members)}명 삭제 중...")
        deleted_count = 0
        for member in existing_members:
            record_id = member.get('gs_record_id') or member.get('id')
            if record_id:
                if delete_member(record_id):
                    deleted_count += 1
                time.sleep(0.1)  # Rate limiting
        
        print(f"✅ {deleted_count}명 삭제 완료")
    else:
        print("ℹ️ 삭제할 기존 멤버 없음")
    
    # 4. 새 멤버 추가
    print(f"\n➕ 새 멤버 {len(new_members)}명 추가 중...")
    added_count = 0
    failed_count = 0
    
    for i, member in enumerate(new_members, 1):
        # DB에 저장할 데이터 형식으로 변환
        member_data = {
            "nickname": member.get("nickname", ""),
            "job": member.get("job", ""),
            "power": member.get("combat_power", 0),
            "server": member.get("server", "아스펠")
        }
        
        if create_member(member_data):
            added_count += 1
            print(f"  [{i}/{len(new_members)}] ✅ {member_data['nickname']} ({member_data['job']}) - {member_data['power']}")
        else:
            failed_count += 1
            print(f"  [{i}/{len(new_members)}] ❌ {member_data['nickname']}")
        
        # Rate limiting
        time.sleep(0.1)
    
    # 5. 결과 출력
    print("\n" + "=" * 60)
    print("📊 동기화 결과:")
    print(f"  ✅ 추가 성공: {added_count}명")
    print(f"  ❌ 추가 실패: {failed_count}명")
    print(f"  📝 총 처리: {len(new_members)}명")
    print("=" * 60)
    
    if added_count > 0:
        print("\n🎉 DB 동기화 완료!")
        print(f"모든 사용자가 최신 {added_count}명의 길드 멤버를 확인할 수 있습니다.")
        return True
    else:
        print("\n❌ DB 동기화 실패!")
        return False

# ==========================
# 메인 실행
# ==========================

def main():
    """메인 실행 함수"""
    
    # JSON 파일 존재 확인
    if not os.path.exists('region_members.json'):
        print("❌ region_members.json 파일을 찾을 수 없습니다.")
        print("먼저 collect_region.py를 실행하세요.")
        exit(1)
    
    # DB 동기화 실행
    success = sync_members_to_db()
    
    if success:
        exit(0)
    else:
        exit(1)

if __name__ == "__main__":
    main()
