from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Load API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/generate_faq', methods=['POST'])
def generate_faq():
    data = request.json
    topic = data.get('topic', 'General')
    prompt = f"Generate FAQs for the topic: {topic}. Be professional."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return jsonify(response['choices'][0]['message']['content'])

if __name__ == '__main__':
    app.run(debug=True)
