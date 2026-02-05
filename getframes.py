import os
import cv2

input_dir = os.getcwd()
output_root = os.path.join(input_dir, "frames")
os.makedirs(output_root, exist_ok=True)

for file in os.listdir(input_dir):
    if file.endswith(".mp4"):
        video_path = os.path.join(input_dir, file)
        base_name = os.path.splitext(file)[0]
        output_dir = os.path.join(output_root, base_name)

        # Check if folder exists and contains any .jpg
        if os.path.exists(output_dir) and any(fname.endswith(".jpg") for fname in os.listdir(output_dir)):
            print(f"[!] Skipping {file} — frames already extracted.")
            continue

        os.makedirs(output_dir, exist_ok=True)
        print(f"[•] Extracting frames from {file}...")

        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        interval = int(fps * 2)  # every 2 seconds

        frame_count = 0
        saved_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if frame_count % interval == 0:
                frame_path = os.path.join(output_dir, f"frame_{saved_count:04d}.jpg")
                cv2.imwrite(frame_path, frame)
                saved_count += 1
            frame_count += 1

        cap.release()
        print(f"[✓] {saved_count} frames saved → {output_dir}")
