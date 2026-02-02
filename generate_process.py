import os
from text_to_audio import text_to_speech_file

def text_to_audio(folder):
    print("TAR - ", folder)
    with open(f"user_uploads/{folder}/text.txt") as f:
        text = f.read()
    print(text, folder)
    # text_to_speech_file(text, folder)

def create_reel(folder):
    print("CR - ", folder)


if __name__ == "__main__":
    with open("done.txt", "r") as f:
        done_folders = f.readlines()

    done_folders = [f.strip() for f in done_folders]
    folders = os.listdir("user_uploads")
    for folder in folders:
        if(folder not in done_folders):
            text_to_audio(folder)
            create_reel(folder)
            with open("done.txt", "a") as f:
                f.write(folder + "\n")