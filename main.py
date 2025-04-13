pip install openai sounddevice numpy pyttsx3

import openai
import sounddevice as sd
import numpy as np
import pyttsx3
import tempfile
import wave

# OpenAI API keyini buraya yaz
openai.api_key = "OPEN AI API "

# Sesli yanıt motoru
engine = pyttsx3.init()
engine.setProperty('voice', 'com.apple.speech.synthesis.voice.Alex')  # macOS erkek sesi


def speak(text):
    engine.say(text)
    engine.runAndWait()


def record_audio(duration=5, fs=44100):
    print("🎙️ Dinleniyor...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()

    # Geçici bir wav dosyasına kaydet
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        with wave.open(f.name, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # int16 = 2 byte
            wf.setframerate(fs)
            wf.writeframes(recording.tobytes())
        return f.name


def whisper_transcribe(audio_file_path):
    print("🧠 Ses yazıya dönüştürülüyor...")
    with open(audio_file_path, "rb") as f:
        transcript = openai.Audio.transcribe("whisper-1", f)
    return transcript['text']


def ask_chatgpt(question):
    print("🤖 ChatGPT düşünüyor...")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # gpt-4 varsa onu da kullanabilirsin
        messages=[
            {"role": "system", "content": "Sen akıllı bir yapay zekâ asistansın."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message['content']


# === ANA DÖNGÜ ===
while True:
    speak("Hey Mert, ne öğrenmek istersin?")
    audio_path = record_audio(duration=5)
    question = whisper_transcribe(audio_path)

    print("🗨️ Sen dedin ki:", question)

    if question.strip() == "":
        speak("Seni duyamadım.")
        continue

    answer = ask_chatgpt(question)
    print("💬 Jarvis:", answer)
    speak(answer)
