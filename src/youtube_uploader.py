import os
import json
import time
import urllib.request
import urllib.error

def get_valid_access_token():
    token_json_str = os.getenv('YOUTUBE_TOKEN_JSON')
    if not token_json_str:
        print('[YouTube] YOUTUBE_TOKEN_JSON secret not set.')
        return None
    try:
        data = json.loads(token_json_str)
        client_id = data['client_id']
        client_secret = data['client_secret']
        refresh_token = data['refresh_token']
        
        rurl = 'https://oauth2.googleapis.com/token'
        pdata = json.dumps({
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }).encode('utf-8')
        rreq = urllib.request.Request(rurl, data=pdata, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(rreq, timeout=30) as rresp:
            res = json.loads(rresp.read().decode('utf-8'))
            return res.get('access_token')
    except Exception as e:
        print(f'[YouTube] Error refreshing access token: {e}')
        return None

def upload_short_to_youtube(video_path: str, title: str, description: str, tags: list):
    access_token = get_valid_access_token()
    if not access_token:
        print('[YouTube] Cannot upload: Access token not available.')
        return False
        
    try:
        file_size = os.path.getsize(video_path)
        print(f'[YouTube] Uploading {os.path.basename(video_path)} ({file_size} bytes) to YouTube...')
        
        # 1. Initiate resumable upload
        init_url = 'https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status'
        metadata = {
            'snippet': {
                'title': title[:98],
                'description': f'{description}\n\n#shorts #gta6 #viral',
                'tags': tags if isinstance(tags, list) else [t.strip('#') for t in tags.split()],
                'categoryId': '20' # Gaming
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False
            }
        }
        
        init_req = urllib.request.Request(
            init_url,
            data=json.dumps(metadata).encode('utf-8'),
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json; charset=UTF-8',
                'X-Upload-Content-Type': 'video/mp4',
                'X-Upload-Content-Length': str(file_size)
            },
            method='POST'
        )
        
        with urllib.request.urlopen(init_req, timeout=30) as init_resp:
            upload_url = init_resp.headers.get('Location')
            
        if not upload_url:
            print('[YouTube] Failed to get resumable upload URL.')
            return False
            
        print('[YouTube] Uploading video data...')
        with open(video_path, 'rb') as f:
            video_bytes = f.read()
            
        up_req = urllib.request.Request(
            upload_url,
            data=video_bytes,
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'video/mp4',
                'Content-Length': str(file_size)
            },
            method='PUT'
        )
        
        with urllib.request.urlopen(up_req, timeout=120) as up_resp:
            result = json.loads(up_resp.read().decode('utf-8'))
            video_id = result.get('id')
            print(f'[YouTube] SUCCESS! Video published! Link: https://youtube.com/shorts/{video_id}')
            return f'https://youtube.com/shorts/{video_id}'
            
    except Exception as e:
        print(f'[YouTube] Upload failed: {e}')
        return False
