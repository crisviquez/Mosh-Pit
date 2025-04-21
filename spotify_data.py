from auth import sp

def search_artist(artist_name):
    results = sp.search(q=artist_name, limit=1, type="artist")
    if results['artists']['items']:
        return results['artists']['items'][0]['id']
    else:
        print("❌ No existe este artiste we")

def get_artist_album(artist_id):
    album = sp.artist_albums(artist_id=artist_id, limit=20)
    for i in range(min(12, len(album['items']))):
        print(album['items'][i]['name'])

def get_all_albums_by_artist(artist_id):
    all_albums = []
    seen_album_names = set()
    results = sp.artist_albums(artist_id=artist_id, album_type='album', limit=50)

    while True:
        for album in results['items']:
            name = album['name']
            if name not in seen_album_names:
                all_albums.append({
                    'name': name,
                    'uri': album['uri'],
                    'release_date': album['release_date']
                })
                seen_album_names.add(name)
        if results['next']:
            results = sp.next(results)
        else:
            break

    return all_albums

def get_most_recent_album(artist_id):
    album = sp.artist_albums(artist_id=artist_id, limit=1, album_type='album')
    return album['items'][0]['uri']

def get_top_tracks(range_limit, range_time):
    top_tracks = sp.current_user_top_tracks(limit=range_limit, time_range=range_time)
    print("🎵 Tus canciones más escuchadas:")
    for i, track in enumerate(top_tracks['items'], start=1):
        print(f"{i}. {track['name']} - {track['artists'][0]['name']}")

def get_top_artists(range_limit, range_time):
    top_artist = sp.current_user_top_artists(limit=range_limit, time_range=range_time)
    print("🎵 Tus artistas más escuchadas:")
    for i, artist in enumerate(top_artist['items'], start=1):
        print(f"{i}. {artist['name']}")

def get_top_track_uris(limit, time_range):
    top_tracks = sp.current_user_top_tracks(limit=limit, time_range=time_range)
    return [track['uri'] for track in top_tracks['items']]

def get_song_duration(track_uri):
    track = sp.track(track_uri)
    ms = track['duration_ms']
    minutes = ms // 60000
    seconds = (ms % 60000) // 1000
    return f"{minutes}:{seconds:02d}"

def get_recommendations_from_track(track_id, limit=5):
    recommendations = sp.recommendations(seed_tracks=[track_id], limit=limit)
    return [
        {'name': track['name'], 'artist': track['artists'][0]['name'], 'uri': track['uri']}
        for track in recommendations['tracks']
    ]

def get_album_release_dates(artist_id):
    albums = get_all_albums_by_artist(artist_id)
    return [(album['name'], album['release_date']) for album in albums]

def like_current_song():
    current = sp.current_playback()
    if current and current['is_playing']:
        track_id = current['item']['id']
        sp.current_user_saved_tracks_add([track_id])
        return True
    return False

def get_current_playing():
    current = sp.current_playback()
    if current and current['is_playing']:
        track = current['item']
        return {
            'name': track['name'],
            'artist': track['artists'][0]['name']
        }
    return None

def search_playlist_by_name(name):
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:
        if name.lower() in playlist['name'].lower():
            return playlist['uri']
    return None

def search_tracks(query, limit=5):
    results = sp.search(q=query, type='track', limit=limit)
    tracks = []
    for track in results['tracks']['items']:
        tracks.append({
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'uri': track['uri']
        })
    return tracks

def search_playlists(query, limit=5):
    results = sp.search(q=query, type='playlist', limit=limit)
    playlists = []
    for playlist in results['playlists']['items']:
        playlists.append({
            'name': playlist['name'],
            'uri': playlist['uri'],
            'owner': playlist['owner']['display_name']
        })
    return playlists