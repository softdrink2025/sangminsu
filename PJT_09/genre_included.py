import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import musicbrainzngs as mb
import json
from data.models import Track, Genre

client_id = '3c9d7c27a8fc4870ad2ee601957018e7'
client_secret = '92b5af97fffc47b9821989244352c48e'

client_credentials_manager = SpotifyClientCredentials(client_id= client_id, client_secret= client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# JSON 형식의 API를 반복을 통해 리스트에 담고, 각 리스트에 담긴 데이터를 JSON 파일로 저장하는 과정입니다.
track_data = []

# MusicBrainz API 설정
mb.set_useragent("MyApp", "1.0", "your_email@example.com")  # 사용자 정보 설정
for i in range(0, 100, 50):
    track_results = sp.search(q='track', type='track', limit=50, offset=i)
    for t in track_results['tracks']['items']:
        track_db = Track()
        track_db.track_name = t['name']
        track_db.track_id = t['id']
        track_db.track_popularity = t['popularity']
        track_db.artist_name = t['artists'][0]['name']
        track_db.artist_id = t['artists'][0]['id']
        track_db.release_year = t['album']['release_date']
        track_db.duration_ms = t['duration_ms']
        track_db.track_image_link = t['album']['images'][0]['url']
         

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
        track_name = track_db.track_name
        artist_name = track_db.artist_name

        # 뮤직브레인즈에서 트랙 ID 찾기
        mbid = get_musicbrainz_recording_id(track_name, artist_name)

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
                tags_tuple_list = []
                for tag in tags:
                    # 태그 투표 수, 태그 이름 쌍을 튜플로 저장
                    tags_tuple_list.append((tag['count'], tag['name']))
                # 투표 수를 기준으로 내림차순으로 정렬
                tags_tuple_list.sort(reverse=True)
                
                if len(tags_tuple_list) > 3:
                    for i in range(3):
                        # 해당 장르가 있는 경우
                        if Genre.objects.filter(name=tags_tuple_list[i][1]):
                            track_db.genreId = tags_tuple_list[i][1]
                            track_db.save()     # 장르 추가하고 저장
                        else:   # 없으면 장르 테이블에 추가 후 db에 저장
                            track_genre = Genre()
                            track_genre = tags_tuple_list[i][1]
                            track_genre.save()
                            track_db.genreId = tags_tuple_list[i][1]
                            track_db.save()     # 장르 추가하고 저장
                            
                elif len(tags_tuple_list) <= 3 and len(tags_tuple_list) > 0:
                    for tags_tuple in tags_tuple_list:
                        # 해당 장르가 있는 경우
                        if Genre.objects.filter(name=tags_tuple[1]):
                            track_db.genreId = tags_tuple[1]
                            track_db.save()     # 장르 추가하고 저장
                        else:   # 없으면 장르 테이블에 추가 후 db에 저장
                            track_genre = Genre()
                            track_genre = tags_tuple[1]
                            track_genre.save()
                            track_db.genreId = tags_tuple[1]
                            track_db.save()     # 장르 추가하고 저장
                else:
                    track_db.save()

            else:
                print(f"❌ Recording ID: {recording_id}에는 현재 부여된 태그가 없습니다.")

        except mb.WebServiceError as exc:
            print(f"MusicBrainz API 오류 발생: {exc}")