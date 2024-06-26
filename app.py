import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS


app = Flask(__name__)
CORS(app) 
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/files', methods=['GET'])
def list_files():
    files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.glb')]
    return jsonify(files)

@app.route('/files/<filename>', methods=['GET'])
def get_file(filename):
    # envoyer a mobile app
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400
    
    if file and file.filename.endswith('.glb'):
        # Count existing GLB files in the UPLOAD_FOLDER
        existing_files = os.listdir(app.config['UPLOAD_FOLDER'])
        num_existing_files = len([name for name in existing_files if name.endswith('.glb')])
        
        # Create new filename based on the count
        new_filename = f"Patient{num_existing_files + 1}.glb"
        
        # Save the file to UPLOAD_FOLDER with the new filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        file.save(file_path)
        
        return jsonify({"message": f"File {file.filename} successfully uploaded as {new_filename}"}), 201
    else:
        return jsonify({"error": "Invalid file format. Only .glb files are allowed."}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

