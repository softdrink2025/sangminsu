# import json

# # 기존 JSON 파일 경로
# input_file = 'track_data.json'
# # 수정된 JSON 파일을 저장할 경로
# output_file = 'updated_track_data.json'

# # 앱 이름과 모델 이름을 정의
# app_name = "data"
# model_name = "Track"

# # 기존 JSON 파일 읽기
# with open(input_file, 'r', encoding='utf-8') as file:
#     data = json.load(file)

# # 모델 추가
# for obj in data:
#     obj["model"] = f"{app_name}.{model_name}"

# # 수정된 데이터를 새 파일로 저장
# with open(output_file, 'w', encoding='utf-8') as file:
#     json.dump(data, file, ensure_ascii=False, indent=4)

# print(f"Updated JSON file saved as {output_file}")


# -- try 2 --
# import json

# # 기존 JSON 파일 경로
# input_file = 'updated_track_data.json'
# # 수정된 JSON 파일을 저장할 경로
# output_file = 'fixed_track_data.json'

# # 앱 이름과 모델 이름을 정의
# app_name = "data"
# model_name = "Track"

# # 기존 JSON 파일 읽기
# with open(input_file, 'r', encoding='utf-8') as file:
#     data = json.load(file)

# # 각 항목에 'fields' 추가
# for obj in data:
#     if 'fields' not in obj:
#         obj['fields'] = {}
    
#     # 'fields' 필드를 채워넣기 (모델 필드에 맞게 수정)
#     obj['fields'] = {
#         "track_name": obj.get('track_name', ""),
#         "track_id": obj.get('track_id', ""),
#         "track_popularity": obj.get('track_popularity', 0),
#         "artist_name": obj.get('artist_name', ""),
#         "artist_id": obj.get('artist_id', ""),
#         "release_year": obj.get('release_year', ""),
#         "duration_ms": obj.get('duration_ms', 0),
#         "track_image_link": obj.get('track_image_link', "")
#     }

#     # 모델 정보 추가
#     obj['model'] = f"{app_name}.{model_name}"

# # 수정된 데이터를 새 파일로 저장
# with open(output_file, 'w', encoding='utf-8') as file:
#     json.dump(data, file, ensure_ascii=False, indent=4)

# print(f"Updated JSON file saved as {output_file}")

# -- try 3 --

import json

# 기존 JSON 파일 경로
input_file = 'track_data.json'
# 수정된 JSON 파일을 저장할 경로
output_file = 'last_track_data.json'

# 앱 이름과 모델 이름을 정의
app_name = "data"
model_name = "Track"

# 기존 JSON 파일 읽기
with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 각 항목에 대해 수정
for obj in data:
    # model 필드 추가
    obj["model"] = f"{app_name}.{model_name}"
    
    # 'fields' 필드를 추가하여 중복 제거
    if "fields" not in obj:
        obj["fields"] = {}
    
    # 'fields' 필드에 실제 모델 필드만 추가
    obj["fields"] = {
        "track_name": obj.get("track_name", ""),
        "track_id": obj.get("track_id", ""),
        "track_popularity": obj.get("track_popularity", 0),
        "artist_name": obj.get("artist_name", ""),
        "artist_id": obj.get("artist_id", ""),
        "release_year": obj.get("release_year", ""),
        "duration_ms": obj.get("duration_ms", 0),
        "track_image_link": obj.get("track_image_link", "")
    }

    # 불필요한 기존 데이터를 삭제 (중복 제거)
    obj.pop("track_name", None)
    obj.pop("track_id", None)
    obj.pop("track_popularity", None)
    obj.pop("artist_name", None)
    obj.pop("artist_id", None)
    obj.pop("release_year", None)
    obj.pop("duration_ms", None)
    obj.pop("track_image_link", None)

# 수정된 데이터를 새 파일로 저장
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(f"Updated JSON file saved as {output_file}")