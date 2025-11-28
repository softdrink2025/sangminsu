# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials
# import json

# client_id = '3c9d7c27a8fc4870ad2ee601957018e7'
# client_secret = '92b5af97fffc47b9821989244352c48e'

# client_credentials_manager = SpotifyClientCredentials(client_id= client_id, client_secret= client_secret)
# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# # JSON 형식의 API를 반복을 통해 리스트에 담고, 각 리스트에 담긴 데이터를 JSON 파일로 저장하는 과정입니다.
# track_data = []

# for i in range(0, 100, 50):
#     track_results = sp.search(q='track', type='track', limit=50, offset=i)
#     for t in track_results['tracks']['items']:
#         # 아티스트 정보를 통해 장르 정보 가져오기
#         artist_id = t['artists'][0]['id']
#         artist_info = sp.artist(artist_id)  # 아티스트 정보 가져오기
#         genres = artist_info['genres']  # 장르 정보 가져오기

#         track_info = {
#             'track_name': t['name'],
#             'track_id': t['id'],
#             'track_popularity': t['popularity'],
#             'artist_name': t['artists'][0]['name'],
#             'artist_id': artist_id,
#             'release_year': t['album']['release_date'],  # 앨범 출시 년도
#             'duration_ms': t['duration_ms'],  # 트랙 재생 시간 (밀리초)
#             'track_image_link': t['album']['images'][0]['url'],
#             'genres': genres  # 장르 정보 추가
#         }
#         track_data.append(track_info)

# # JSON 파일로 저장
# with open('test.json', 'w', encoding='utf-8') as json_file:
#     json.dump(track_data, json_file, ensure_ascii=False, indent=4)




import musicbrainzngs as mb

# MusicBrainz API 설정
mb.set_useragent("MyApp", "1.0", "your_email@example.com")  # 사용자 정보 설정
# musicbrainzngs.set_format("json")

def get_musicbrainz_recording_id(track_name, artist_name):
    try:
        # 트랙명과 아티스트명으로 뮤직브레인즈에서 검색
        result = mb.search_recordings(track_name, artist=artist_name, limit=5)
        
        # 첫 번째 검색 결과에서 recording ID 추출
        recordings = result.get('recording-list', [])
        if recordings:
            return recordings[0]['id']  # 첫 번째 녹음의 ID 반환
        else:
            return None  # 해당 트랙이 없으면 None 반환
    except mb.WebServiceError as e:
        print(f"WebServiceError: {e}")
        return None

# 예시: 스포티파이에서 가져온 트랙 정보
track_name = "Blow Your Mind (Mwah)"
artist_name = "Dua Lipa"

# 뮤직브레인즈에서 트랙 ID 찾기
mbid = get_musicbrainz_recording_id(track_name, artist_name)

if mbid:
    print(f"MusicBrainz Recording ID: {mbid}")
else:
    print("Track not found on MusicBrainz.")


# 획득한 Recording ID를 변수에 저장합니다. (예: Dua Lipa의 Blow Your Mind (Mwah))
recording_id = mbid

try:
    # 💥 get_recording_by_id 함수를 사용하고 includes=['tags']를 명시합니다.
    result = mb.get_recording_by_id(
        recording_id, 
        includes=['tags']  
    )
    
    # 결과에서 'recording' 키 아래의 'tag-list'를 추출합니다.
    tags = result['recording'].get('tag-list', [])
    
    if tags:
        print(f"✅ Recording ID: {recording_id}의 태그 목록:")
        for tag in tags:
            # 태그 이름과 투표 수(count)를 출력합니다.
            print(f"- {tag['name']} (Count: {tag['count']})")
    else:
        print(f"❌ Recording ID: {recording_id}에는 현재 부여된 태그가 없습니다.")

except mb.WebServiceError as exc:
    print(f"MusicBrainz API 오류 발생: {exc}")