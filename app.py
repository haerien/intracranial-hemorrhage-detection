import os
import time
import torch
import zipfile
from flask import Flask, render_template, request, redirect, jsonify
from werkzeug.utils import secure_filename
from torchvision import transforms
from PIL import Image
from transformers import AutoModelForImageClassification, AutoFeatureExtractor

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load the model and feature extractor from Hugging Face
model_name = "DifeiT/rsna-intracranial-hemorrhage-detection"
model = AutoModelForImageClassification.from_pretrained(model_name)
feature_extractor = AutoFeatureExtractor.from_pretrained(model_name)

# Label mapping dictionary
label_map = {
    0: "epidural",
    1: "intraparenchymal",
    2: "intraventricular",
    3: "normal/none",
    4: "subarachnoid",
    5: "subdural"
}

def convert_image(file_path):
    if file_path.lower().endswith('.jpeg'):
        img = Image.open(file_path)
        new_file_path = file_path.rsplit('.', 1)[0] + '.jpg'
        img = img.convert('RGB')  # Ensure image is in RGB mode
        img.save(new_file_path, 'JPEG')
        os.remove(file_path)  # Remove the original .jpeg file
        return new_file_path
    return file_path

def process_image(file_path):
    file_path = convert_image(file_path)  # Convert .jpeg and .dcm to .jpg if needed
    start_time = time.time()
    image = Image.open(file_path)
    inputs = feature_extractor(images=image, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    predicted_class_idx = logits.argmax(-1).item()
    predicted_label = label_map[predicted_class_idx]
    end_time = time.time()
    predicted_time = end_time - start_time
    return predicted_label, predicted_time

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        results = []
        if zipfile.is_zipfile(file_path):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(app.config['UPLOAD_FOLDER'])
            # Process each file in the ZIP
            for file_name in zip_ref.namelist():
                if file_name.endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif', 'dcm')):
                    full_file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                    result, predicted_time = process_image(full_file_path)
                    results.append((file_name, result, predicted_time))
        else:
            result, predicted_time = process_image(file_path)
            results = [(filename, result, predicted_time)]
        
        # Return the results as JSON
        return jsonify(results=results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000')
