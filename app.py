# app.py
from flask import Flask, request, send_file, render_template, jsonify
import os
from pixel_to_vector import pixel_to_vector
import tempfile

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    num_colors = int(request.form['num_colors'])
    smoothing = float(request.form.get('smoothing', 1.0))
    turdsize = int(request.form.get('turdsize', 2))
    
    try:
        # Save uploaded file temporarily
        _, temp_input_path = tempfile.mkstemp(suffix='.png')
        file.save(temp_input_path)
        
        # Create temporary output file
        _, temp_output_path = tempfile.mkstemp(suffix='.svg')
        
        # Run conversion
        pixel_to_vector(temp_input_path, num_colors, temp_output_path, smoothing, turdsize)
        
        # Send file to user
        return send_file(temp_output_path, as_attachment=True, download_name='converted.svg', mimetype='image/svg+xml')
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up temporary files
        os.remove(temp_input_path)
        os.remove(temp_output_path)

if __name__ == '__main__':
    app.run(debug=True)
