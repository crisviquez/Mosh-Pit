from auth import sp

def pause_playback():
    try:
        sp.pause_playback()
        print("⏸️ Reproducción pausada.")
    except Exception as e:
        print("❌ Error al pausar:", e)

def resume_playback():
    try:
        sp.start_playback()
        print("▶️ Reproducción reanudada.")
    except Exception as e:
        print("❌ Error al reanudar:", e)

def next_track():
    try:
        sp.next_track()
        print("⏭️ Siguiente canción.")
    except Exception as e:
        print("❌ Error al avanzar:", e)

def previous_track():
    try:
        sp.previous_track()
        print("⏮️ Canción anterior.")
    except Exception as e:
        print("❌ Error al retroceder:", e)

def set_volume(volume):
    try:
        sp.volume(volume)
        print(f"🔊 Volumen ajustado a {volume}%")
    except Exception as e:
        print("❌ Error al ajustar volumen:", e)

def toggle_shuffle(state=True):
    try:
        sp.shuffle(state)
        estado = "activado" if state else "desactivado"
        print(f"🔀 Modo aleatorio {estado}.")
    except Exception as e:
        print("❌ Error al cambiar modo aleatorio:", e)