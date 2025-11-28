import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

client_id = '3c9d7c27a8fc4870ad2ee601957018e7'
client_secret = '92b5af97fffc47b9821989244352c48e'

client_credentials_manager = SpotifyClientCredentials(client_id= client_id, client_secret= client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# JSON 형식의 API를 반복을 통해 리스트에 담고, 각 리스트에 담긴 데이터를 JSON 파일로 저장하는 과정입니다.
track_data = []

# for i in range(0, 1000, 50):
#     track_results = sp.search(q='year:2021', type='track', limit=50, offset=i)
#     for t in track_results['tracks']['items']:
#         track_info = {
#             'track_name': t['name'],
#             'track_id': t['id'],
#             'track_popularity': t['popularity'],
#             'artist_name': t['artists'][0]['name'],
#             'artist_id': t['artists'][0]['id'],
#             'release_year': t['album']['release_date'],  # 앨범 출시 년도
#             'duration_ms': t['duration_ms'],  # 트랙 재생 시간 (밀리초)
#             'track_image_link': t['album']['images'][0]['url'],
#         }
#         track_data.append(track_info)

# # JSON 파일로 저장
# with open('track_data.json', 'w', encoding='utf-8') as json_file:
#     json.dump(track_data, json_file, ensure_ascii=False, indent=4)

for i in range(0, 100, 50):
    track_results = sp.search(q='track', type='track', limit=50, offset=i)
    for t in track_results['tracks']['items']:
        track_info = {
            'track_name': t['name'],
            'track_id': t['id'],
            'track_popularity': t['popularity'],
            'artist_name': t['artists'][0]['name'],
            'artist_id': t['artists'][0]['id'],
            'release_year': t['album']['release_date'],  # 앨범 출시 년도
            'duration_ms': t['duration_ms'],  # 트랙 재생 시간 (밀리초)
            'track_image_link': t['album']['images'][0]['url'],
        }
        track_data.append(track_info)

# JSON 파일로 저장
with open('track_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(track_data, json_file, ensure_ascii=False, indent=4)
