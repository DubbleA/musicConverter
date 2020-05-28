from __future__ import unicode_literals
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from youtube_search import YoutubeSearch
import time
import json
import youtube_dl


LINK = "your soundcloud link"
SKIPPED = []

class Song:
    def __init__(self, n, a):
        self.name = n
        self.artist = a

def sc_parse(link):
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(link)
    time.sleep(1)
    elem = browser.find_element_by_tag_name("body")

    no_of_pagedowns = 20

    while no_of_pagedowns:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
        no_of_pagedowns -= 1

        names = browser.find_elements_by_class_name("trackItem__trackTitle")
        artists = browser.find_elements_by_class_name("trackItem__username")

    names = soupParser(names)
    artists = soupParser(artists)
    songs = []

    for i in range(0, len(names)):
        song = Song(names[i], artists[i])
        string = f'{song.artist} - {song.name}'
        songs.append(string)

    return songs

def soupParser(cParsed):
    array = []
    for post in cParsed:
        array.append(post.text)

    return array

def getLink(songName):
    results = YoutubeSearch(songName, max_results=1).to_json()
    #print(results)
    results = json.loads(results)
    if(len(results['videos']) > 0):

        #print(results['videos'][0]['title'])
        return results['videos'][0]
    else:
        print(" ")
        print("retrying " + songName)

        results = YoutubeSearch(songName, max_results=1).to_json()
        #print(results)
        results = json.loads(results)
        if (len(results['videos']) < 1):
            print("skipped " + songName)
            SKIPPED.append(songName)
        else:
            return results['videos'][0]


def youtubeExtract(link):
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,  # only keep the audio
        'audioformat': "mp3",  # convert to mp3
        #'outtmpl': '%(id)s',   name the file the ID of the video
        'noplaylist': True,  # only download single song, not playlist

        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("downloading" + link)
        ydl.download(['http://www.youtube.com' + link])


def main():
    yt_titles = []
    links = []
    songs = sc_parse(LINK)
    print(songs)

    for i in range(len(songs)):

        results = getLink(songs[i])

        yt_titles.append(results['title'])
        links.append(results['link'])

    print(yt_titles)
    print(links)

    for i in range (0, len(songs)):
        print(" ")
        print(songs[i])
        print(yt_titles[i])
        print(" ")

    for i in range(len(links)):
        youtubeExtract(links[i])


if __name__ == '__main__':
    main()



