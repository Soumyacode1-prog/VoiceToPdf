import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print("Say something...")
    audio = r.listen(source)
    print("Captured audio")

try:
    text = r.recognize_google(audio)
    print("Recognized:", text)
except sr.UnknownValueError:
    print("❌ Could not understand audio")
except sr.RequestError as e:
    print("🚫 API error:", e)
except Exception as e:
    print("⚠️ Other error:", e)