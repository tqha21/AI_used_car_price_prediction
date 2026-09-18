import os, uuid
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
from PIL import Image

upload_bp = Blueprint('upload', __name__)

ALLOWED = {'png', 'jpg', 'jpeg', 'webp'}
MAX_SIZE_MB = 5

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED

def get_upload_dir():
    d = os.path.join(current_app.static_folder, 'uploads')
    os.makedirs(d, exist_ok=True)
    return d

@upload_bp.route('/upload/image', methods=['POST'])
@login_required
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'Không tìm thấy file.'}), 400
    f = request.files['file']
    if not f.filename or not allowed_file(f.filename):
        return jsonify({'error': 'Chỉ chấp nhận jpg, png, webp.'}), 400
    content = f.read()
    if len(content) > MAX_SIZE_MB * 1024 * 1024:
        return jsonify({'error': f'File vượt quá {MAX_SIZE_MB}MB.'}), 400
    ext      = f.filename.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    save_path = os.path.join(get_upload_dir(), filename)
    # Resize to max 1200px width to save storage
    from io import BytesIO
    img = Image.open(BytesIO(content)).convert('RGB')
    if img.width > 1200:
        ratio = 1200 / img.width
        img = img.resize((1200, int(img.height * ratio)), Image.LANCZOS)
    img.save(save_path, quality=85, optimize=True)
    url = f"/static/uploads/{filename}"
    return jsonify({'url': url, 'filename': filename})
