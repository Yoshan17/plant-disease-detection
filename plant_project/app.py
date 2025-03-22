from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import base64
import os

app = Flask(__name__)

# Gemini API key (ඔබේ API key එක මෙතන දාන්න්)
GEMINI_API_KEY = "AIzaSyB14xbJG7D3c8N3jZBGc8IMwKYKmkIS4xs"
genai.configure(api_key=GEMINI_API_KEY)

# Gemini model setup
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "Please upload an image!"}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "Please select an image!"}), 400

        # Image එක base64 එකට encode කරන්න්
        image_data = file.read()
        encoded_image = base64.b64encode(image_data).decode('utf-8')

        # Gemini API එකට request එක යවන්න්
        prompt = """
        Analyze this plant image and identify any diseases. Provide the following details in English:
        - Disease: The name of the disease.
        - Symptoms: The visible symptoms of the disease.
        - Treatment: The recommended treatment for the disease, including specific methods like cultural practices, organic treatments, or chemical treatments.
        If treatment information is unavailable, suggest consulting a local agricultural expert.
        Format the response as:
        Disease: [disease name]
        Symptoms: [symptoms]
        Treatment: [treatment]
        """
        response = model.generate_content([
            prompt,
            {"inline_data": {"mime_type": "image/jpeg", "data": encoded_image}}
        ])

        # Response එක process කරන්න්
        response_text = response.text
        # Response එක parse කරන්න්
        disease_info = {
            "disease": "Not detected",
            "symptoms": "Not detected",
            "treatment": "Consult a local agricultural expert for treatment recommendations."
        }
        
        lines = response_text.split('\n')
        for line in lines:
            if line.startswith("Disease:"):
                disease_info["disease"] = line.replace("Disease:", "").strip()
            elif line.startswith("Symptoms:"):
                disease_info["symptoms"] = line.replace("Symptoms:", "").strip()
            elif line.startswith("Treatment:"):
                treatment = line.replace("Treatment:", "").strip()
                # Treatment එක empty නම් default message එක තියෙනවා
                disease_info["treatment"] = treatment if treatment else "Consult a local agricultural expert for treatment recommendations."

        return jsonify({
            "disease": disease_info["disease"],
            "symptoms": disease_info["symptoms"],
            "treatment": disease_info["treatment"],
            "yellow_percentage": "N/A",
            "image_url": None
        })

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)