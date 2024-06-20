# Import modules
from ollama import Client
from waitress import serve
from flask import Flask, render_template, request

# Initialise Flask app
app = Flask(__name__)
# Initialise OpenAI client
client = Client(host='http://192.168.1.221:11434')

# Function to generate idea
def generate_idea(language, hours, extra_info, model="llama3"):
    # Set prompt message
    message = f"give me one idea for a {language} project that will take {hours} hours to complete. Give the idea in 5 words or less. Do not output anything except the answer. {extra_info}"
    # Generate response
    response = client.generate(prompt=message, model=model)
    response = response['response']
    return response

# route for index.html
@app.route('/', methods=['GET', 'POST'])
def index():
    generated_idea = ""
    if request.method == 'POST':
        # Get form data
        language = request.form['language']
        hours = request.form['hours']
        extra_info = request.form['extra_info']
        generated_idea = generate_idea(language, hours, extra_info)
    # Render template
    return render_template('index.html', generated_idea=generated_idea)

# Main function
if __name__ == '__main__':
    app.run(debug=True)