import spotipy
import spotipy.util as util
import calendar
from datetime import datetime, timedelta
import itertools

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

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

longest_time = 0
offending_songs = ''
hall_of_fame = []

for i in pairwise(song_list):
    print(i)
    a = i[0]
    b = i[1]

    diff = b['added_at'] - a['added_at']
    t = timedelta(seconds=diff)
    print_diff = "Time to Keep: {}m-{}d {}".format(t.days/30, t.days%30, timedelta(seconds=t.seconds))
    distance = a['track']['name'] + '->' + b['track']['name'] + '=' + print_diff
    print(distance)

    if a['track']['name']!=b['track']['name'] and diff > longest_time:
        longest_time = diff
        offending_songs = distance

    hall_of_fame.append((distance, diff))

hall_of_fame.sort(key=lambda tup: tup[1])

for i in hall_of_fame:
    print(i)
