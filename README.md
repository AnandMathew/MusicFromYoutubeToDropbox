# MusicFromYoutubeToDropbox

## Synopsis   

Polls your youtube account every 4 hours for a list of liked videos. It then compares the list to a previously polled list to discover any new liked videos. It then uses [youtube-dl](https://github.com/rg3/youtube-dl) to download the video as a m4a file if it is a music video under Creative Common Licence.
Consequently, the service uploads the m4a file to your Dropbox under the folder "music".

Ideally, once you start the service and let it run, all you have to do is like videos for it to eventually show up in your Dropbox.

## Setup

Please install [youtube-dl](https://github.com/rg3/youtube-dl)

Please get a client_id and client_secret from google and replace the values in client_secret.json. Better yet, generate a json with your credentials and rename it to client_secret.json

Please also get a Dropbox api key from Dropbox

run `python getLikedVideos.py`

The CLI will prompt you for an authorization code and provide you a link that you need to enter your web browser in order to go through Google's authentication flow. Once you get the code after authenticating with Google, and enter it into the CLI, the program will start.

## Licensing Information

The software is available under the MIT license. 


