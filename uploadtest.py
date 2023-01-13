from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import requests
  
def refresh_access_token():
    # Set the API endpoint and request parameters
    endpoint = 'https://oauth2.googleapis.com/token'
    data = {
    'client_secret': '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',
    'grant_type': 'refresh_token',
    'refresh_token': '1//04OPW9e4h1CMuCgYIARAAGAQSNwF-L9IrgjICJoAcm4qx4ROhxlHuDvKo2PdeKKS5f68SIAdFSLfpce_wkTGKfWHnJq5ZoFdHldc',
    'client_id': '164520596220-leevtqd6pgh5vhnv799s17chkm5ukd3d.apps.googleusercontent.com'
    }

    # Send the POST requestṇ
    response = requests.post(endpoint, data=data)

    # Extract the access token from the response
    access_token = response.json()['access_token']

    return access_token



access_token = 'ya29.a0AX9GBdVk0JXVIuk4rXk5TBIEvLR_A2bCnfUpU6XvMhQJcWd5CfyW957rya0qQuj621rDfUETNng1-69FXwXkHafJOp7FjazArj_vTaEHRiTZIDQI9EMsg9e0Cl_auDEolkOuRO6-8qN7dLB7KKZq8SRpoAABFFEaCgYKAZASAQASFQHUCsbCD3RZY29k5dU1RuPFdJ-Kvg0166'
info = {
    'client_id': '164520596220-leevtqd6pgh5vhnv799s17chkm5ukd3d.apps.googleusercontent.com',
    'client_secret': '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',
    'refresh_token': '1//04pkJxC-teRa3CgYIARAAGAQSNwF-L9Iry2KuWbf162AatYpaY0xiqZNCqaWGfvWKaqMCspiIhlA1fjmfLH4vOiexApbiVMzg3nA',
    'access_token': access_token
}


creds = Credentials.from_authorized_user_info(info=info)
youtube = build('youtube', 'v3', credentials=creds)
video_metadata = {
  'snippet': {
    'title': 'My Video',
    'description': 'This is my video.',
    'tags': ['my', 'video'],
    'categoryId': 22
  },
  'status': {
    'privacyStatus': 'private'
  }
}
# Create the video
request = youtube.videos().insert(
  part='snippet,status',
  body=video_metadata,
  media_body=MediaFileUpload('video.mp4', mimetype='video/mp4')
)
response = request.execute()
print(response)


# https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=ya29.a0AX9GBdUYs0Bod_FuFXXOwYEkKCsJhGNXQgu-NTXlg14A_cc4_ZW1HgVSeSXsdk2YzbN7eJyG_L0V6BX5jF9NkgzqS1Jwi7Hv8spWjAAmJ1ItskboTveaccjgf0CghPveP_MrxqUm0yCinBe-ql3IK-kKTvjFaCgYKAW8SARISFQHUCsbCc-zEkqizXrpOkEfPOzU3Pw0163