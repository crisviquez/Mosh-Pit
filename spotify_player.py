from auth import sp

def play_song(song_name):
    results = sp.search(q=song_name, limit=1, type='track')
    if results['tracks']['items']:
        track_uri = results['tracks']['items'][0]['uri']
        print(f"🎶 Reproduciendo: {results['tracks']['items'][0]['name']}")
        sp.start_playback(uris=[track_uri])
    else:
        print("❌ Canción no encontrada.")

def play_album(album_uri):
    album_tracks = sp.album_tracks(album_id=album_uri)
    track_uris = [track['uri'] for track in album_tracks['items']]
    if track_uris:
        sp.start_playback(uris=track_uris)
        print("🎧 Reproduciendo álbum completo.")
    else:
        print("❌ No se encontraron canciones en el álbum.")

def play_playlist(playlist_uri):
    devices = sp.devices()
    if not devices['devices']:
        print("❌ No hay dispositivos activos. Abre Spotify en algún dispositivo y vuelve a intentarlo.")
        return
    try:
        sp.start_playback(context_uri=playlist_uri)
        print(f"▶️ Reproduciendo playlist: {playlist_uri}")
    except Exception as e:
        print("❌ Error al reproducir la playlist:", e)
