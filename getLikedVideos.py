
import os
import downloadSongs
import uploadMusic
import time
import schedule

import google.oauth2.credentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

pageToken = ""
videoIds = []
prevVideoIds = []
newVideoIds = []

def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def videos_list_my_rated_videos(service, **kwargs):
  kwargs = remove_empty_kwargs(**kwargs)

  response = service.videos().list(
    **kwargs
  ).execute()
  
  for likedVideo in response['items']:
      if likedVideo and (likedVideo['snippet']['categoryId'] == "10" or likedVideo['snippet']['categoryId'] == "24") and (likedVideo['contentDetails']['licensedContent'] is not True):
          videoIds.append(likedVideo['id']) 
          
  try:
    if response['nextPageToken'] is not None :
        pageToken = response['nextPageToken']
        videos_list_my_rated_videos(service,
        part='snippet,contentDetails,statistics',
        myRating='like',
        pageToken=pageToken)
  except KeyError :
      return
    

def remove_empty_kwargs(**kwargs):
  good_kwargs = {}
  if kwargs is not None:
    for key, value in kwargs.iteritems():
      if value:
        good_kwargs[key] = value
  return good_kwargs

def compareIds(prevIds,currentIds,newIds):
    for id in currentIds:
        if id not in prevIds:
            newIds.append(id)


def updateArray(prevIds,currentIds):
    for id in currentIds:
        if id not in prevIds:
            prevIds.append(id)

if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    service = get_authenticated_service()

    def job():
        print "Starting new poll for liked videos........"
        updateArray(prevVideoIds,videoIds)
        del videoIds[:]
        videos_list_my_rated_videos(service,
            part='snippet,contentDetails,statistics',
            myRating='like'
            )
        
        # print "Previous Video Ids: "
        # print ', '.join(prevVideoIds)
        # print "Current Video Ids: "
        # print ', '.join(videoIds)

        compareIds(prevVideoIds,videoIds,newVideoIds)
        if (len(prevVideoIds) == 0):
            print "not downloading songs because prev video list is empty"
            del newVideoIds[:]

        print "New Video Ids: "
        print ', '.join(newVideoIds)

        downloadSongs.youtubeDlSongs(newVideoIds)
        uploadMusic.uploadToDropbox()
        del newVideoIds[:]

    job();
    schedule.every(4).hours.do(job);

    while True:
        schedule.run_pending()
        time.sleep(1)
