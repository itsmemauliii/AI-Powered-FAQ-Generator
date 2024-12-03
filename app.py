from flask import Flask, render_template, request, redirect, url_for
from models import db, BusinessDetails, FAQ, FAQGenerationLog
import openai
from datetime import datetime
import os

app = Flask(__name__)

# Initialize the app with database URL and other configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///faqs.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

# OpenAI API key should ideally be loaded from an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_faq', methods=['POST'])
def generate_faq():
    business_name = request.form['business_name']
    description = request.form['description']
    category = request.form['category']

    # Ensure OpenAI API key is set
    if not openai.api_key:
        return "Error: OpenAI API key is not set."

    # Prepare prompt for generating FAQs
    prompt = f"Generate a list of FAQs for a business named {business_name} in the {category} category. Description: {description}"

    try:
        # Call OpenAI API to generate FAQs
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )

        # Parse the response
        faqs = []
        for choice in response.choices:
            # Example of processing text - assuming it's split into question and answer
            faq_text = choice.text.strip().split('\n')
            if len(faq_text) > 1:
                faqs.append({
                    'question': faq_text[0],  # First line is question
                    'answer': faq_text[1]     # Second line is answer
                })

    except Exception as e:
        return f"Error generating FAQs: {e}"

    # Save FAQ data to database
    business = BusinessDetails.query.filter_by(name=business_name).first()
    if not business:
        business = BusinessDetails(name=business_name, description=description)
        db.session.add(business)
        db.session.commit()

    # Add generated FAQs to the database
    for faq in faqs:
        new_faq = FAQ(question=faq['question'], answer=faq['answer'], business_id=business.id)
        db.session.add(new_faq)

    db.session.commit()

    # Log the FAQ generation
    log = FAQGenerationLog(business_id=business.id, generated_at=datetime.now(), num_faqs=len(faqs))
    db.session.add(log)
    db.session.commit()

    # Return the generated FAQs and render the results page
    return render_template('faq_results.html', business_name=business_name, faqs=faqs)

if __name__ == "__main__":
    app.run(debug=True)
