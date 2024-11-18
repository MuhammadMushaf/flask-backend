import requests

def upload_video(file_path):
    url = "https://api.mux.com/video/v1/uploads"
    headers = {
        "Authorization": "Bearer MUX_ACCESS_TOKEN"  ##Add mux token here
    }
    data = {
        "new_asset_settings": {
            "playback_policy": ["public"]
        }
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()
