import spotipy
import spotipy.util as util
import calendar
from datetime import datetime
import itertools

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)

    diff = b['added_at'] - a['added_at']
    d = datetime(1,1,1) + diff
    print_diff = "%d:%d:%d:%d" % (d.day-1, d.hour, d.minute, d.second)

    print(b['name'] + '->' + a['name'] + '=' + print_diff)

username = '***REMOVED***'
scope = 'playlist-read-collaborative'
user = '***REMOVED***'
song_list = []

token = util.prompt_for_user_token(username, scope, client_id='***REMOVED***', client_secret='***REMOVED***', redirect_uri='http://localhost/')

if token:
    sp = spotipy.Spotify(auth=token)   
    results = sp.user_playlist_tracks(user, playlist_id='***REMOVED***', fields="items.track.name,items.added_at,next")
    song_list = song_list + results['items']

    while(results['next']!=None):
        results = sp.next(results)
        song_list = song_list + results['items']
else:
    print("Can't get token for", username)

for song in song_list:

    print(song)
    datetime_object = datetime.strptime(song['added_at'], '%Y-%m-%dT%H:%M:%SZ')
    song['added_at'] = calendar.timegm(datetime_object.utctimetuple())
    print(song)

pairwise(song_list)
