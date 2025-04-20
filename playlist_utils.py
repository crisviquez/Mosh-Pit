from auth import sp

def create_wrapped_playlist(name, description, track_uris):
    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user=user_id, name=name, public=True, description=description)
    sp.playlist_add_items(playlist['id'], track_uris)
    print(f"✅ Playlist '{name}' creada con éxito.")
    return playlist['uri']

def list_my_playlists():
    playlists = sp.current_user_playlists()
    print("📂 Tus playlists:")
    for playlist in playlists['items']:
        print(f"- {playlist['name']} (ID: {playlist['id']})")
