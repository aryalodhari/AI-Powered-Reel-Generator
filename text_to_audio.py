import os
from dotenv import load_dotenv
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

if not ELEVENLABS_API_KEY:
    raise ValueError("❌ ELEVENLABS_API_KEY not found in .env")

elevenlabs = ElevenLabs(api_key=ELEVENLABS_API_KEY)


def text_to_speech_file(text: str, folder: str) -> str:
    if not text or not text.strip():
        print("❌ Empty text — skipping audio generation")
        return ""

    save_dir = os.path.join("user_uploads", folder)
    os.makedirs(save_dir, exist_ok=True)

    save_file_path = os.path.join(save_dir, "audio.mp3")

    print("🎙 Generating audio...")

    try:
        response = elevenlabs.text_to_speech.convert(
            voice_id="pNInz6obpgDQGcFmaJgB",
            output_format="mp3_22050_32",
            text=text,
            model_id="eleven_turbo_v2_5",
            voice_settings=VoiceSettings(
                stability=0.3,
                similarity_boost=0.8,
                style=0.0,
                use_speaker_boost=True,
                speed=1.0,
            ),
        )

        with open(save_file_path, "wb") as f:
            for chunk in response:
                if chunk:
                    f.write(chunk)

        print(f"✅ Audio saved: {save_file_path}")
        return save_file_path

    except Exception as e:
        print("❌ ElevenLabs error:", e)
        return ""
