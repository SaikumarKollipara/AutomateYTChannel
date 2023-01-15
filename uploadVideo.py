import http
import httplib2
import random
import requests
import time

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import googleapiclient



# Explicitly tell the underlying HTTP transport library not to retry, since we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, http.client.NotConnected,
  http.client.IncompleteRead, http.client.ImproperConnectionState,
  http.client.CannotSendRequest, http.client.CannotSendHeader,
  http.client.ResponseNotReady, http.client.BadStatusLine)

# Always retry when an apiclient.errors.HttpError with one of these status codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# This OAuth 2.0 access scope allows an application to upload files to the authenticated user's YouTube channel, but doesn't allow other types of access.
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")

# Set the chunk size to 10MB (10485760 bytes).
CHUNK_SIZE = 10485760


def refresh_access_token(refresh_token):
    # Set the API endpoint and request parameters
    endpoint = 'https://oauth2.googleapis.com/token'
    data = {
    'client_secret': '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',
    'grant_type': 'refresh_token',
    'refresh_token': refresh_token,
    'client_id': '164520596220-leevtqd6pgh5vhnv799s17chkm5ukd3d.apps.googleusercontent.com'
    }

    # Send the POST request
    response = requests.post(endpoint, data=data)

    # Extract the access token from the response
    access_token = response.json()['access_token']

    return access_token



# Set the access token.
REFRESH_TOKEN = '1//04Ff8B7MhZWiWCgYIARAAGAQSNwF-L9IruojbZefFbDSsbnQrCb6a1XLsm9SNqrlagS7hw7ATcmUKQt-Gufc2mZDXS9apgAfRDMU'
ACCESS_TOKEN = refresh_access_token(REFRESH_TOKEN)

def get_authenticated_service():
    info = { 'client_id': '164520596220-leevtqd6pgh5vhnv799s17chkm5ukd3d.apps.googleusercontent.com', 'client_secret': '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', 'refresh_token': REFRESH_TOKEN, 'access_token': ACCESS_TOKEN }
    creds = Credentials.from_authorized_user_info(info=info)
    youtube = build('youtube', 'v3', credentials=creds)
    return youtube

def initialize_upload(youtube, file, metadata):
    body = {
        'snippet': metadata,
        'status': {
            'privacyStatus': 'private'
        }
    }
    # Call the API's videos.insert method to create and upload the video.
    insert_request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=googleapiclient.http.MediaFileUpload(
            file, chunksize=CHUNK_SIZE, resumable=True)
    )
    resumable_upload(insert_request)


# This method implements an exponential backoff strategy to resume a failed upload.
def resumable_upload(insert_request):
  response = None
  error = None
  retry = 0
  while response is None:
    try:
      print("Uploading file...")
      status, response = insert_request.next_chunk()
      if response is not None:
        if 'id' in response:
          print("Video id '%s' was successfully uploaded." % response['id'])
        else:
          exit("The upload failed with an unexpected response: %s" % response)
    except HttpError as e:
      if e.resp.status in RETRIABLE_STATUS_CODES:
        error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                             e.content)
      else:
        raise
    except RETRIABLE_EXCEPTIONS as e:
      error = "A retriable error occurred: %s" % e

    if error is not None:
      print(error)
      retry += 1
      if retry > MAX_RETRIES:
        exit("No longer attempting to retry.")

      max_sleep = 2 ** retry
      sleep_seconds = random.random() * max_sleep
      print("Sleeping %f seconds and then retrying..." % sleep_seconds)
      time.sleep(sleep_seconds)





if __name__ == '__main__':

    youtube = get_authenticated_service()
    try:
        # Set the file and metadata for the video that you want to upload.
        file = 'video.mp4'
        metadata = {
            'title': 'My Video',
            'description': 'This is my video.'
        }
        # Call the API's videos.insert method to create and upload the video.
        initialize_upload(youtube, file, metadata)
    except HttpError as error:
        print('An HTTP error %d occurred:\n%s' % (error.resp.status, error.content))
