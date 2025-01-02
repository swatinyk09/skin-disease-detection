from flask import Flask, request, render_template, jsonify, redirect, url_for, flash
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__)
app.secret_key = 'qwert'  # Required for session and flash messages

# Simulating a database (for accounts)
users = {"swati":"asdfg"}

# Load your pre-trained Keras model
model = load_model('.\\models\\model.keras')

# Define the classes of skin diseases
class_names = ['akiec', 'bcc', 'bkl', 'df', 'mel', 'nv', 'vasc']

# Ensure upload directory exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to preprocess the image
def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(75, 100))  # Adjust based on model input
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array /= 255.0  # Normalize
    return img_array

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if not file.filename.lower().endswith(('png', 'jpg', 'jpeg')):
        return jsonify({'error': 'Invalid file type. Only PNG, JPG, JPEG allowed.'})

    # Save file to a temporary location
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        # Preprocess the image and predict
        img_array = preprocess_image(filepath)
        prediction = model.predict(img_array)
        predicted_class = class_names[np.argmax(prediction)]
        confidence = round(float(np.max(prediction)) * 100, 2)         
        
        # Information about skin diseases
        skin_disease_info = {
            "akiec": "Actinic Keratoses and Intraepithelial Carcinoma: Precancerous skin lesions caused by sun damage. Actinic Keratoses are rough, scaly patches caused by prolonged sun exposure. They can develop into squamous cell carcinoma if untreated. Intraepithelial carcinoma refers to early-stage cancer that remains confined to the top layer of the skin, making early detection crucial.",
            "bcc": "Basal Cell Carcinoma: Basal cell carcinoma is the most common form of skin cancer. It typically appears as a shiny, pearly bump, a red patch, or a non-healing sore, primarily in sun-exposed areas like the face and neck. Though it grows slowly and rarely spreads, prompt treatment is necessary to prevent local tissue damage.",
            "bkl": "Benign Keratosis-like Lesions: Benign keratosis-like lesions include harmless skin growths such as seborrheic keratosis or solar lentigo. These lesions often appear as brown, tan, or black spots and are common in older adults. While they are non-cancerous, distinguishing them from malignant lesions may require professional evaluation.",
            "df": "Dermatofibroma: Dermatofibroma is a benign skin growth, often appearing as a small, firm, raised bump that may feel tender or itchy. They are generally harmless and can result from minor skin injuries or insect bites, commonly occurring on the legs or arms.",
            "mel": "Melanoma: Melanoma is a serious form of skin cancer that arises from melanocytes, the pigment-producing cells. It may appear as a new or existing mole with irregular borders, uneven color, or increasing size. Early detection and treatment are critical, as melanoma can spread rapidly to other parts of the body.",
            "nv": "Melanocytic Nevi: Melanocytic nevi, commonly known as moles, are benign growths of melanocytes. They can range in color from pink to dark brown and vary in size. While most moles are harmless, any changes in appearance should be checked for potential malignancy.",
            "vasc": "Vascular Lesions: Vascular lesions include conditions like hemangiomas or angiomas, which result from abnormal blood vessels. These lesions may appear as red or purple spots on the skin and are typically benign. In some cases, they may require treatment for cosmetic reasons or discomfort."
        }

        # Get detailed information for the predicted class
        disease_info = skin_disease_info.get(predicted_class, "Information not available.")

        # Render the dashboard with prediction and info
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'})
    finally:
        # Clean up uploaded file
        os.remove(filepath)

    return jsonify({'predicted_class': predicted_class, 'confidence': float(confidence), 'info': disease_info})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/help')
def help_page():
    return render_template('help.html')

@app.route('/account', methods=['GET', 'POST'])
def account():
    if request.method == 'POST':
        form_type = request.form.get('form_type')

        # Handle login
        if form_type == 'login':
            username = request.form['username']
            password = request.form['password']
            if username in users and users[username] == password:
                flash('Login successful!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password.', 'danger')

        # Handle registration
        elif form_type == 'register':
            username = request.form['username']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            if username in users:
                flash('Username already exists.', 'danger')
            elif password != confirm_password:
                flash('Passwords do not match.', 'danger')
            else:
                users[username] = password
                flash('Registration successful! You can now log in.', 'success')
                return redirect(url_for('account'))

    return render_template('account.html')

@app.route('/consultancy')
def consultancy():
    return render_template('consultancy.html')

if __name__ == '__main__':
    app.run(debug=True)
