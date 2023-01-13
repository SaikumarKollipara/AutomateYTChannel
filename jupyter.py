from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from time import sleep
from datetime import timedelta

options = Options()
# options.headless = True
driver = webdriver.Chrome(options=options, executable_path=r'C:\webdrivers\chromedriver.exe')


driver.get('https://kaggle.com')
sleep(2)
print('browser opened')

#signIn button
driver.find_element_by_css_selector('#site-container > div:nth-child(1) > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) a').click()
sleep(2)
# email signin
driver.find_element_by_css_selector('form > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) a').click()
#email & pass
sleep(2)
email = driver.find_element_by_css_selector('[name="email"]')
email.send_keys('kkrksaikumar@gmail.com')
email.send_keys(Keys.ENTER)
password = driver.find_element_by_css_selector('[name="password"]')
password.send_keys('Skumar@123')
password.send_keys(Keys.ENTER)
sleep(2)

# Go to notebook
driver.get('https://www.kaggle.com/code/krksaikumar/automateytchannel/edit')
print('notebook opened')
sleep(35)
print('Page loaded successfully')

installationCode = '''!pip install moviepy
!pip install pillar-youtube-upload
'''

codeToGenerateAndUploadVideo = '''import os
from moviepy.editor import *

path = '/kaggle/input/clips'
clips = os.listdir(path)
video = concatenate_videoclips([ VideoFileClip(os.path.join(path, clip)).without_audio() for clip in clips ], method='compose')
video = video.resize(width=1920,height=1080)

hours = 2
minutes = 0
reqDuration = (hours * 60 + minutes) * 60
finalVideo = video.loop(duration=reqDuration)

music = AudioFileClip('/kaggle/input/audio/relaxing.mp3')
audio = afx.audio_loop(music, duration=reqDuration)
finalVideo = finalVideo.set_audio(audio)


finalVideo.write_videofile('video.mp4', codec='libx264')



# upload to youtube
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import requests    

access_token = 'ya29.a0AX9GBdVk0JXVIuk4rXk5TBIEvLR_A2bCnfUpU6XvMhQJcWd5CfyW957rya0qQuj621rDfUETNng1-69FXwXkHafJOp7FjazArj_vTaEHRiTZIDQI9EMsg9e0Cl_auDEolkOuRO6-8qN7dLB7KKZq8SRpoAABFFEaCgYKAZASAQASFQHUCsbCD3RZY29k5dU1RuPFdJ-Kvg0166'
info = { 'client_id': '164520596220-leevtqd6pgh5vhnv799s17chkm5ukd3d.apps.googleusercontent.com', 'client_secret': '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', 'refresh_token': '1//04VvWrKVTLjcDCgYIARAAGAQSNwF-L9IrSEG9lhVPZ0OYzXDY_NUxPAyqMH1MxLZ0fBECcmz62THfiBBX1akLXfTzoiM5no-knVg', 'access_token': access_token }
creds = Credentials.from_authorized_user_info(info=info)
youtube = build('youtube', 'v3', credentials=creds)
video_metadata = { 'snippet': { 'title': 'My Video', 'description': 'This is my video.', 'tags': ['my', 'video'], 'categoryId': 22 }, 'status': { 'privacyStatus': 'private' } }


media = MediaFileUpload('video.mp4', mimetype='video/mp4', resumable=True)
media.chunksize = 10 * 1024 * 1024
request = youtube.videos().insert( part='snippet,status', body=video_metadata, media_body=media )
response = None
while response is None:
status, response = request.next_chunk()
if status: print(f'Uploaded {int(status.progress() * 100)}%')
print(response)'''


def generateAndUpload():
    # paste installationCode and shift + enter to execute cell
    action = ActionChains(driver)
    action.send_keys(installationCode).key_down(Keys.LEFT_SHIFT).send_keys(Keys.ENTER).key_up(Keys.LEFT_SHIFT).perform()
    sleep(60)

    # delete the two cells
    driver.find_element_by_css_selector('[title="Delete cell"]').click()
    driver.find_element_by_css_selector('[title="Delete cell"]').click()
    sleep(3)

    # restart and clear outputs
    driver.find_element_by_css_selector('[title="Toggle sidebar visibility"]').click()
    driver.find_element_by_css_selector('[title="More"]').click()
    sleep(3)
    driver.find_element_by_css_selector('#rmwcPortal > div:nth-child(2) > ul > li:nth-child(3)').click()
    sleep(3)
    driver.find_element_by_css_selector('[title="Delete cell"]').click()
    sleep(2)
    action = ActionChains(driver)
    action.send_keys(Keys.TAB).perform()
    
    # paste codeToGenerateAndUploadVideo and shift + enter to execute cell
    action = ActionChains(driver)
    action.send_keys(codeToGenerateAndUploadVideo).key_down(Keys.LEFT_CONTROL).send_keys(Keys.DIVIDE).key_up(Keys.LEFT_CONTROL).key_down(Keys.LEFT_SHIFT).send_keys(Keys.ENTER).key_up(Keys.LEFT_SHIFT).perform()

    # keep browser open to generate video
    sleep(7 * 60 * 60)

    # delete the two cells
    driver.find_element_by_css_selector('[title="Delete cell"]').click()
    driver.find_element_by_css_selector('[title="Delete cell"]').click()


try:
    generateAndUpload()
except Exception as e:
    print(e)
    exit()