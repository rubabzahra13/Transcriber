import os
import whisper

# Load the model once
model = whisper.load_model("base")

# Create transcripts directory
output_dir = "transcripts"
os.makedirs(output_dir, exist_ok=True)

# Get all MP4 video files
video_files = [f for f in os.listdir() if f.endswith(".mp4")]

# Loop through each video
for video in sorted(video_files):
    print(f"[→] Transcribing {video} ...")

    try:
        result = model.transcribe(video)
        text = result["text"]

        # Save to txt file inside transcripts/
        txt_filename = os.path.splitext(video)[0] + ".txt"
        txt_path = os.path.join(output_dir, txt_filename)

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"[✓] Saved transcript to {txt_path}")

    except Exception as e:
        print(f"[!] Error while transcribing {video}: {e}")
