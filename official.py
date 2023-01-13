#!/usr/bin/python


import httplib2
import os
import random
import sys
import time

from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

import argparse
import http
import httplib2
import os
import random
import time

import google.oauth2.credentials
import google_auth_oauthlib.flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient


# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
# RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, httplib.NotConnected,
#   httplib.IncompleteRead, httplib.ImproperConnectionState,
#   httplib.CannotSendRequest, httplib.CannotSendHeader,
#   httplib.ResponseNotReady, httplib.BadStatusLine)

RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, http.client.NotConnected,
  http.client.IncompleteRead, http.client.ImproperConnectionState,
  http.client.CannotSendRequest, http.client.CannotSendHeader,
  http.client.ResponseNotReady, http.client.BadStatusLine)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the Google API Console at
# https://console.cloud.google.com/.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secrets.json"

# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of access.
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.


VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")


# Set the access token.
ACCESS_TOKEN = 'ya29.a0AX9GBdUYs0Bod_FuFXXOwYEkKCsJhGNXQgu-NTXlg14A_cc4_ZW1HgVSeSXsdk2YzbN7eJyG_L0V6BX5jF9NkgzqS1Jwi7Hv8spWjAAmJ1ItskboTveaccjgf0CghPveP_MrxqUm0yCinBe-ql3IK-kKTvjFaCgYKAW8SARISFQHUCsbCc-zEkqizXrpOkEfPOzU3Pw0163'
REFRESH_TOKEN = '1//04yPsA4Qu_mwYCgYIARAAGAQSNwF-L9IrZM3AqRe4yuXdwX4V_1NGLt23nI5rQasUMkNPLNyFUi6hZX1-pFIURrMwZrGwgXfP6UI'

# Set the chunk size to 10MB (10485760 bytes).
CHUNK_SIZE = 10485760

def get_authenticated_service():
    # # Create an HTTP header with the access token.
    # headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN}

    # # Build the service object using the authorized headers.
    # youtube = googleapiclient.discovery.build('youtube', 'v3',
    #     http=googleapiclient.discovery.Http(headers=headers))


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


# This method implements an exponential backoff strategy to resume a
# failed upload.
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
