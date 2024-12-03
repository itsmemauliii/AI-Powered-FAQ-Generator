import openai

openai.api_key = "your_openai_api_key"

prompt = "Generate FAQs for an e-commerce business."
prompt = "List the most common questions about [product/service]."
prompt = "How can I troubleshoot [issue] related to [product/service]?"
prompt = "Provide clear, concise FAQs for a [type of business]."
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)
print(response['choices'][0]['message']['content'])
