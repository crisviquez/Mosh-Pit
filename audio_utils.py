import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[3].id)

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

def decir(texto):
    engine.say(texto)
    engine.runAndWait()
