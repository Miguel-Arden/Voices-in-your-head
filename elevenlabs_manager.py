import os
import time
from elevenlabs import ElevenLabs, Voice, stream, save, play

# Initialize ElevenLabs client directly with the API key
API_KEY = os.getenv('ELEVENLABS_API_KEY')  # Make sure this environment variable is set
client = ElevenLabs(api_key=API_KEY)

class ElevenLabsManager:
    def __init__(self):
        # fetch and display all available voices
        try:
            voices = Voice.list()  # fetch all available voices
            print("\nAvailable voices:\n")
            for voice in voices:
                print(f"- {voice.name} (ID: {voice.id})")
        except Exception as e:
            print("Error fetching voices:", str(e))

    # Convert text to speech, then save it to file. Returns the file path
    def text_to_audio(self, input_text, voice_name="Rachel", voice_id=None, save_as_wave=False, subdirectory=""):
        try:
            if voice_id:
                voice = Voice(voice_id=voice_id)
            else:
                voice = voice_name
            audio_stream = client.generate(
                text=input_text,
                voice=voice,
                model="eleven_flash_v2_5",
                stream=False
            )
            if save_as_wave:
                file_name = f"Msg_{hash(input_text)}.wav"
            else:
                file_name = f"Msg_{hash(input_text)}.mp3"

            tts_file = os.path.join(os.path.abspath(os.curdir), subdirectory, file_name)
            save(audio_stream, tts_file)
            return tts_file
        except Exception as e:
            print("Error generating audio:", str(e))
            return None

    # Convert text to speech, then play it out loud
    def text_to_audio_played(self, input_text, voice_name="Rachel", voice_id=None):
        try:
            if voice_id:
                voice = Voice(voice_id=voice_id)
            else:
                voice = voice_name
            audio_stream = client.generate(
                text=input_text,
                voice=voice,
                model="eleven_flash_v2_5",
                stream=True
            )
            play(audio_stream)
        except Exception as e:
            print("Error playing audio:", str(e))

    # Convert text to speech, then stream it out loud
    def text_to_audio_streamed(self, input_text, voice_name="Rachel", voice_id=None):
        try:
            if voice_id:
                voice = Voice(voice_id=voice_id)
            else:
                voice = voice_name
            audio_stream = client.generate(
                text=input_text,
                voice=voice,
                model="eleven_flash_v2_5",
                stream=True
            )
            stream(audio_stream)
        except Exception as e:
            print("Error streaming audio:", str(e))

if __name__ == '__main__':
    # Create an instance of the manager
    elevenlabs_manager = ElevenLabsManager()

    # Test streaming audio
    elevenlabs_manager.text_to_audio_streamed(
        "This is a test of streaming audio. Let's see if it works!", 
        voice_name="Rachel"
    )
    time.sleep(2)

    # Test playing audio
    elevenlabs_manager.text_to_audio_played(
        "Now we're playing this text as audio. Sounds good, right?", 
        voice_name="Rachel"
    )
    time.sleep(2)

    # Test saving audio to a file
    file_path = elevenlabs_manager.text_to_audio(
        "Finally, this audio is being saved to a file. Great job!",
        voice_name="Rachel"
    )
    if file_path:
        print(f"Audio saved to: {file_path}")

    print("All tests complete. Waiting for a bit before exiting...")
    time.sleep(10)
