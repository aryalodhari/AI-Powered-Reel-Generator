import os
import subprocess
from text_to_audio import text_to_speech_file

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "user_uploads")

def text_to_audio(folder):
    print("TAR -", folder)
    text_path = os.path.join(UPLOAD_DIR, folder, "text.txt")

    if not os.path.exists(text_path):
        print("❌ text.txt missing")
        return

    with open(text_path, "r", encoding="utf-8") as f:
        text = f.read()

    print(text)
    text_to_speech_file(text, folder)
    audio_path = os.path.join(UPLOAD_DIR, folder, "audio.mp3")
    if not os.path.exists(audio_path):
        print("❌ Audio generation failed, skipping reel")
        return

def create_reel(folder):
    folder_path = os.path.join(UPLOAD_DIR, folder)

    input_txt = "input.txt"
    audio_file = "audio.mp3"
    output_file = "reel.mp4"

    if not os.path.exists(os.path.join(folder_path, input_txt)):
        print("❌ input.txt missing:", folder)
        return

    if not os.path.exists(os.path.join(folder_path, audio_file)):
        print("❌ audio.mp3 missing:", folder)
        return

    print("▶ Running FFmpeg in:", folder_path)
    print("📄 Files:", os.listdir(folder_path))

    command = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", input_txt,
        "-i", audio_file,
        "-vf",
        "scale=1080:1920:force_original_aspect_ratio=decrease,"
        "pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        "-r", "30",
        "-pix_fmt", "yuv420p",
        output_file
    ]

    subprocess.run(command, cwd=folder_path, check=True)
    print("✅ Reel created:", folder)


if __name__ == "__main__":
    done_file = os.path.join(BASE_DIR, "done.txt")

    done_folders = []
    if os.path.exists(done_file):
        with open(done_file, "r") as f:
            done_folders = [line.strip() for line in f]

    for folder in os.listdir(UPLOAD_DIR):
        if folder not in done_folders:
            text_to_audio(folder)
            create_reel(folder)

            with open(done_file, "a") as f:
                f.write(folder + "\n")
