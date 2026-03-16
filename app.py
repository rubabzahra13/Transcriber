"""
Video Transcriber — Flask backend.
Accepts video uploads, transcribes with Whisper, returns transcript.
"""
import os
import uuid
from pathlib import Path

from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename

# Lazy-load Whisper to avoid slow startup
_model = None

def get_model():
    global _model
    if _model is None:
        import whisper
        _model = whisper.load_model("base")
    return _model


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 500 * 1024 * 1024  # 500 MB
app.config["UPLOAD_FOLDER"] = Path("uploads")
app.config["UPLOAD_FOLDER"].mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {"mp4", "webm", "mov", "avi", "mkv", "m4v"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/transcribe", methods=["POST"])
def transcribe():
    if "video" not in request.files and "file" not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    file = request.files.get("video") or request.files.get("file")
    if not file or file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({
            "error": f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        }), 400

    ext = file.filename.rsplit(".", 1)[1].lower()
    safe_name = f"{uuid.uuid4().hex}.{ext}"
    path = app.config["UPLOAD_FOLDER"] / safe_name

    try:
        file.save(path)
        model = get_model()
        result = model.transcribe(str(path), fp16=False)
        text = result["text"].strip()
    except Exception as e:
        if path.exists():
            path.unlink()
        return jsonify({"error": str(e)}), 500
    finally:
        if path.exists():
            path.unlink(missing_ok=True)

    # Optionally save to transcripts/
    save = request.form.get("save") == "true"
    if save and text:
        os.makedirs("transcripts", exist_ok=True)
        base = secure_filename(Path(file.filename).stem)
        out_path = Path("transcripts") / f"{base}.txt"
        out_path.write_text(text, encoding="utf-8")

    return jsonify({"text": text, "saved": save})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
