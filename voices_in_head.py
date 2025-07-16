import openai
import os
from dotenv import load_dotenv
import time
from pathlib import Path
import random
import whisper
import numpy as np
import queue
from rich import print as rprint
import pyaudio
import threading
from elevenlabs_manager import ElevenLabsManager
import playsound

openai.api_key = os.getenv('OPENAI_API_KEY')

whisper_model = whisper.load_model("base")
audio_queue = queue.Queue()

load_dotenv()

elevenlabs_manager = ElevenLabsManager()

def audio_callback(in_data, frame_count, time_info, status):
    audio_queue.put(in_data)
    return (None, pyaudio.paContinue)

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                stream_callback=audio_callback)

def transcribe_audio():
    audio_buffer = []
    while not audio_queue.empty():
        audio_chunk = audio_queue.get()
        audio_buffer.append(np.frombuffer(audio_chunk, dtype=np.int16))
    if audio_buffer:
        audio_array = np.concatenate(audio_buffer).astype(np.float32) / 32768.0
        return whisper_model.transcribe(audio_array, fp16=False)["text"]
    return ""

def play_audio(file):
    playsound.playsound(file)
    os.remove(file)

def main():
    print("Starting live transcription. Speak into the microphone.")
    stream.start_stream()
    accumulated_text1 = ""
    accumulated_text2 = ""
    try:
        while True:
            time.sleep(2)  #transcribe every 2 seconds
            text = transcribe_audio()
            if text.strip():
                rprint(f"Transcribed: [green]{text}[/green]")
                accumulated_text1 += text + " "
                accumulated_text2 += text + " "
            #check for AI1 response
            if accumulated_text1 and random.random() < 0.35:
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a voice in my head, just be annoying and say random things"}, #I recommend changing this prompt to fit your needs (and the other one)
                        {"role": "user", "content": accumulated_text1.strip()}
                    ],
                    max_tokens=35,
                    temperature=1.0,
                )
                ai_response = response['choices'][0]['message']['content']
                rprint(f"AI Voice 1: [blue]{ai_response}[/blue]")

                audio_file = elevenlabs_manager.text_to_audio(ai_response, voice_id="Hjzqw9NR0xFMYU9Us0DL") #change this to whatever voice id you want to use on 11labs

                threading.Thread(target=play_audio, args=(audio_file,)).start()

                accumulated_text1 = ""
            # check for AI2 response
            if accumulated_text2 and random.random() < 0.35: #check if there's accumulated text for AI Voice and randomly trigger a response with 35% probability
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are another voice in my head, be annoying and just say whatever"}, 
                        {"role": "user", "content": accumulated_text2.strip()}
                    ],
                    max_tokens=35,
                    temperature=1.0,
                )

                ai_response = response['choices'][0]['message']['content']
                rprint(f"AI Voice 2: [red]{ai_response}[/red]")

                audio_file = elevenlabs_manager.text_to_audio(ai_response, voice_id="Zlb1dXrM653N07WRdFW3") #change this ID to whatever voice you have on 11labs

                threading.Thread(target=play_audio, args=(audio_file,)).start()

                accumulated_text2 = ""
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    main()
