from flask import Flask, render_template, request, url_for, send_from_directory, abort
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Directory to store uploaded payload HTML files
UPLOAD_FOLDER = os.path.join(app.root_path, 'payloads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'.html', '.htm'}

def _allowed_file(filename: str) -> bool:
    _, ext = os.path.splitext(filename.lower())
    return ext in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_payload():
    # GET: render a simple upload form
    if request.method == 'GET':
        return render_template('index.html')

    # POST: handle file upload
    if 'file' not in request.files:
        return render_template('index.html', error='No file part in the request.'), 400

    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', error='No file selected.'), 400

    if not _allowed_file(file.filename):
        return render_template('index.html', error='Only .html or .htm files are allowed.'), 400

    filename = secure_filename(file.filename)
    if not filename:
        return render_template('index.html', error='Invalid filename.'), 400

    save_path = os.path.join(UPLOAD_FOLDER, filename)
    try:
        file.save(save_path)
    except Exception as e:
        return render_template('index.html', error=f'Failed to save file: {e}'), 500

    # Show success message on the upload page with a link to the payload
    payload_url = url_for('serve_payload', filename=filename)
    return render_template('index.html', success='Upload successful.', payload_url=payload_url)

@app.route('/payloads/<path:filename>')
def serve_payload(filename):
    # Only serve files from the payloads directory and with allowed extensions
    if not _allowed_file(filename):
        abort(404)
    # send_from_directory will safely serve files under the given directory
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)