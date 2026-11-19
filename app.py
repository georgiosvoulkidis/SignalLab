import os
from flask import Flask, render_template, request, flash, redirect
from helpers import process_audio
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "cs50_signal_lab_secret_key"
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Δημιουργία upload φακέλου αν δεν υπάρχει
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'file' not in request.files:
            flash("No file part provided", "danger")
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash("No file selected", "danger")
            return redirect(request.url)

        if file and file.filename.endswith('.wav'):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            try:
                # DSP Επεξεργασία
                results = process_audio(file_path, filename)
                audio_url = f"uploads/{filename}"
                return render_template("index.html", results=results, filename=filename, audio_url=audio_url)
            except Exception as e:
                flash(f"Error processing audio file: {e}", "danger")
                return redirect(request.url)
        else:
            flash("Please upload a valid .WAV audio file", "warning")
            return redirect(request.url)

    return render_template("index.html", results=None)

if __name__ == "__main__":
    app.run(debug=True)
