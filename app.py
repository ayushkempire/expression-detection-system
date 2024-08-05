from flask import Flask, request, render_template, jsonify, send_from_directory
import os
import uuid
from deepface import DeepFace

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'bmp'}
file_path = ''

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and os.path.splitext(filename)[1][1:].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file and allowed_file(file.filename):
        filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1].lower()
        global file_path
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        response = {
            'file_path': file_path
        }
        
        return jsonify(response)
        
@app.route('/analyze', methods=['GET'])
def analyze():
    # Analyze the image
    result = DeepFace.analyze(file_path, actions=['emotion'], enforce_detection=False, align=False)
    
    dominant_emotion = result[0]['dominant_emotion'].capitalize()
    
    response = {
        'emotion': dominant_emotion
    }
    
    return jsonify(response)
    

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
