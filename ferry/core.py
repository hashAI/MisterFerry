#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import requests
import pytube
from pytube import YouTube
from pprint import pprint


class YouTubeSearch(object):
    def __init__(self, query):
        youtube_api = "https://www.googleapis.com/youtube/v3/search?part=snippet&key={key}&q={query}"
        self.url = youtube_api.format(
                key='AIzaSyCIM4EzNqi1in22f4Z3Ru3iYvLaY8tc3bo',
                query=query
                )

    def search(self):
        resp = requests.get(self.url)
        results = resp.json()
        return results

    def get_channels(self, results):
        pass

    def get_videos(self, results, order_by='relevance', ordering='desc'):
        videos = []
        for item in results.get('items', []):
            _id  = item.get('id', {})
            info = {}
            if _id.get('kind') == 'youtube#video':
                snippet = item.get('snippet', {})
                info['id'] = _id.get('videoId')
                info['url'] = "https://www.youtube.com/watch?v="+_id.get('videoId')
                info['title'] = snippet.get('title', '')
                info['description'] = snippet.get('description', '')
                info['thumbnail_url'] = snippet.get('thumbnails', {}).get('default', {}).get('url', '')
                info['channel_id'] = snippet.get('channelId', '')
                info['channel_title'] = snippet.get('channelTitle', '')
                videos.append(info)
        return videos


class YouTubeDownloader(object):
    def __init__(self, url, path='.'):
        self.yt = YouTube(url)
        self.path = path

    def get_streams(self):
        streams = self.yt.streams.filter(progressive=True).order_by('resolution').all()
        return streams

    def download(self, stream):
        stream.download(self.path, filename='_'.join((self.yt.title).split(' ')))


if __name__ == '__main__':
    #search = YouTubeSearch('Faded Alan Walker')
    #videos = search.get_videos(search.search())
    #print(videos)
    stream = YouTubeDownload('https://www.youtube.com/watch?v=oEVnq6LIKOM')
    stream.download()

