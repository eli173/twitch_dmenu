#! /usr/bin/env python
# python 3 whatever

#import urllib2
import livestreamer
import subprocess
import json
import requests
#import io
#from gi.repository import GObject
#from gi.repository import GLib
#from gi.repository import Gst

## pacman : gobject-introspection pygobject-devel python-cairo python2-beaker python2-mako python2-markupsafe python-gobject
##  cdparanoia gst-plugins-base libvisual python2-cairo python2-gobject gst-python
## pyobject2-devel python2-gobject gstreamer0.10-python

# giant C-x C-v class

dmenu_list = ['dmenu', '-i', '-nf', '#262626', '-sf', '#F1F1F1', '-nb', '#B9A3E3', '-sb', '#6441A5']


def space_to_plus(string):
    """turns ' ' in string to '+', for URLs"""
    result = ""
    for char in string:
        if (char == ' '):
            result += '+'
        else:
            result += char
    return result


def get_games():
    """Get games being streamed on Twitch, sorted by viewers"""
    url = 'https://api.twitch.tv/kraken/games/top?limit=100'
    headers = {'Content-Type' : 'application/vnd.twitchtv.v2+json'}
    response = requests.get(url,headers=headers)
    if(response.status_code != requests.codes.ok):
        raise Exception("invalid something in get_games")
    json_response = response.json()
    games = []
    for game in json_response['top']:
        games.append(game['game']['name'])
    #print(games)
    return games

def get_streams(game):
    """Gets twitch streams of game, which is a string with the game's name, and returns tuples with channel names and urls"""
    safe_game = space_to_plus(game)
    url =  'https://api.twitch.tv/kraken/streams?game=' + safe_game
    headers = {'Content-Type' : 'application/vnd.twitchtv.v2+json'}
    #print(url)
    response = requests.get(url,headers=headers)
    if (response.status_code != requests.codes.ok):
        raise Exception("invalid something in get_streams")
    # response.status_code == requests.codes.ok
    #response.json()
    #print(response)
    #print(response.text)
    json_response = response.json()
    #print(json_response['streams']['channel']['display_name'])
    #print(json.dumps(json_response,sort_keys=True,indent=4))
    #print(len(json_response['streams']))
    channels = []
    for stream in json_response['streams']:
        channels.append((stream['channel']['display_name'],stream['channel']['url']))
    return channels
    
def get_quality(stream_url):
    streams = livestreamer.streams(stream_url)
    
def dmenu_thingy_pt_1():
    """returns a URL to the page i guess?"""
    games = get_games()
    games_str = '\n'.join(games)
    #games_stdin = io.StringIO(games_str)
    #games_stdin.write(games_str)
    p = subprocess.Popen(dmenu_list,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    games_result_literal = p.communicate(input=games_str.encode())[0]
    games_result = games_result_literal.decode('utf-8')[:-1]
    #print(get_streams(dmenu_result))
    #print(dmenu_result)
    streams = dict(get_streams(games_result))
    stream_names = []
    for k,v in streams.items():
        stream_names.append(k)
    streams_str = '\n'.join(stream_names)
    q = subprocess.Popen(['dmenu','-i'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    stream_result_literal = q.communicate(input=streams_str.encode())[0]
    stream_result = stream_result_literal.decode('utf-8')[:-1]
    qualities_dict = livestreamer.streams(streams[stream_result])
    quals_ls = []
    for entry in qualities_dict.items():
        quals_ls.append(entry[0])
    # for k,v in qualities_dict:
    #     quals_ls.append(k)
    quals_str = '\n'.join(quals_ls)
    r = subprocess.Popen(['dmenu','-i'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    qual_lit = r.communicate(input=quals_str.encode())[0]
    qual_str = qual_lit.decode('utf-8')[:-1]
    quality = qualities_dict[qual_str]
    
    # tryin somethin crazy...
    #v = subprocess.Popen(['vlc',quality.url])
    subprocess.call(['vlc',quality.url])
    
    #thestreamer = livestreamer.Livestreamer()
    #player = LivestreamerPlayer()
    #player.play(quality)
    #return quality
    #return streams[stream_result]
    # streamers = []
    # for stream in streams:
    #     streamers.append(stream[0])
    
    #print(streamers)
    #print(games_stdin.getvalue())
    #subprocess.call('dmenu',stdin=games_stdin)
    #output = subprocess.check_output('echo -e '+games_str+'| dmenu')
    #subprocess.call('dmenu',stdin=games_str)
    #print(games_str)


if __name__ == "__main__":
    dmenu_thingy_pt_1()
