from audio_utils import escuchar_comando, decir
from spotify_player import play_song

if __name__ == "__main__":
    song = escuchar_comando()
    decir(f"Reproduciendo {song} en Spotify.")
    play_song(song)