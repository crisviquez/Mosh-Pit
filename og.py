import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import speech_recognition as sr
import pyttsx3


load_dotenv()

engine = pyttsx3.init()

def escuchar_comando():
    recognizer = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        print("🎤 Di algo...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        comando = recognizer.recognize_google(audio, language="es-ES")
        print(f"🔊 Dijiste: {comando}")
        return comando.lower()
    except sr.UnknownValueError:
        print("❌ No entendí lo que dijiste.")
        return ""
    except sr.RequestError:
        print("❌ Error al conectarse al servicio de reconocimiento de voz.")
        return ""




# Objeto sp (permisos a Spotify)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    redirect_uri=os.getenv('REDIRECT_URI'),
    scope="user-read-playback-state,user-modify-playback-state,user-read-currently-playing,user-top-read,playlist-modify-public,playlist-modify-private"
))

def play_song(song_name):
    # Buscar la canción en Spotify
    results = sp.search(q=song_name, limit=1, type='track')
    if results['tracks']['items']:
        track_uri = results['tracks']['items'][0]['uri']
        print(f"Reproduciendo: {results['tracks']['items'][0]['name']}")
        sp.start_playback(uris=[track_uri])
    else:
        print("Canción no encontrada.")


def search_artist(artist_name):
    # Buscar el Artista
    results = sp.search(q=artist_name, limit=1, type="artist")
    if results['artists']['items']:
        return results['artists']['items'][0]['id']
    else:
        print("No existe este artiste we")


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


def get_artist_album(artist__id):
    album = sp.artist_albums(artist_id=artist__id, limit=20)
    for i in range(min(12, len(album['items']))):
        print(album['items'][i]['name'])
        

def get_all_albums_by_artist(artist_id):
    all_albums = []
    # Este conjunto nos ayuda a evitar álbumes duplicados por nombre
    seen_album_names = set()
    results = sp.artist_albums( artist_id=artist_id, album_type='album', limit=50)

    while True:
        # Recorremos los álbumes encontrados
        for album in results['items']:
            album_name = album['name']
            album_uri = album['uri']
            release_date = album['release_date']

            # Si no lo hemos agregado todavía (para evitar repetidos)
            if album_name not in seen_album_names:
                all_albums.append({
                    'name': album_name,
                    'uri': album_uri,
                    'release_date': release_date})
                seen_album_names.add(album_name)

        # Si hay una "siguiente página" de resultados, la pedimos
        if results['next']:
            results = sp.next(results)
        else:
            break

    return all_albums

def get_most_recent_album(artist__id):
    album = sp.artist_albums(artist_id=artist__id, limit=1, album_type='album')
    return album['items'][0]['uri']

def play_album(album_uri):
    album_tracks = sp.album_tracks(album_id=album_uri)

    track_uris = []
    for track in album_tracks['items']:
        track_uri = track['uri']
        track_uris.append(track_uri)
    
    if len(track_uris) > 0:
        sp.start_playback(uris=track_uris)
        print("Reproduciendo álbum completo.")
    else:
        print("No se encontraron canciones en el álbum.")


def get_top_tracks(range_limit, range_time):
    top_tracks = sp.current_user_top_tracks(limit=range_limit, time_range=range_time) #short_term (últimos 4 semanas) medium_term (últimos 6 meses) long_term (último año)
    print("🎵 Tus canciones más escuchadas:")
    i=0
    for track in top_tracks['items']:
        name = track['name']
        artist = track['artists'][0]['name']
        i = i+1
        print(f"{i}. {name} - {artist}")

def get_top_artists(range_limit, range_time):
    top_artist = sp.current_user_top_artists(limit=range_limit, time_range=range_time) #short_term (últimos 4 semanas) medium_term (últimos 6 meses) long_term (último año)
    print("🎵 Tus artistas más escuchadas:")
    i=0
    for artist in top_artist['items']:
        i=i+1
        print(f"{i}. {artist['name']}")

def create_wrapped_playlist(name, description, track_uris):
    user_id = sp.me()['id']

    playlist = sp.user_playlist_create(user=user_id, name=name, public=True, description=description)
    playlist_id = playlist['id']

    sp.playlist_add_items(playlist_id, track_uris)
    print(f"✅ Playlist '{name}' creada con éxito.")

    return playlist['uri']

def get_top_track_uris(limit, time_range):
    top_tracks = sp.current_user_top_tracks(limit=limit, time_range=time_range)
    track_uris = []
    for track in top_tracks['items']:
        track_uri = track['uri']
        track_uris.append(track_uri)
    return track_uris    

def list_my_playlists():
    playlists = sp.current_user_playlists()
    print("Tus playlists:")
    for playlist in playlists['items']:
        print(f"- {playlist['name']} (ID: {playlist['id']})")

# Ejemplo de uso:
#print(get_all_albums_by_artist(search_artist("Bad Bunny"))[0]['uri'])
#play_album(get_most_recent_album(search_artist("Eladio")))
#get_top_tracks(20, 'short_term')
#get_top_artists(20, 'medium_term')

#uris = get_top_track_uris(50, 'short_term')
#newplaylist_uri = create_wrapped_playlist('Top 50 canciones en el año', 'quien pone descripciones no mamen', uris)
#play_playlist(newplaylist_uri)
#list_my_playlists()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[3].id)

song = escuchar_comando()
engine.say(f" Reproduciendo {song} en Spotify.")
engine.runAndWait()
play_song(song)