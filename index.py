

from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure your Gemini API Key
genai.configure(api_key='AIzaSyBS7wF1TKGwgAMshAjDuUEwoYRbqSzucbM')  # Replace with your key or use os.environ.get()

# Model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",  # or "gemini-2.5-pro-preview-05-06" if available
    generation_config=generation_config,
)

# Start a session with predefined role and behavior
chat_session = model.start_chat(history=[
    {
        "role": "user",
        "parts": [
            """you are a chatbot, an assistant who works for the postal service. It is involved in delivering mail (post), remitting money by money orders, accepting deposits under Small Savings Schemes, providing life insurance coverage under Postal Life Insurance (PLI) and Rural Postal Life Insurance (RPLI), and providing retail services like bill collection, sale of forms, etc.
Your job is to provide information and answer questions related to postal services briefly and in points in the output and list of schemes in points when asked about the schemes and do ask back the user if any information is required in the above-listed points. Provide brief information or just the names at first and then ask them if they need more information about any of those listed ones. The output should always be in points with numbers for necessary information.
postal services website: https://www.indiapost.gov.in/vas/Pages/IndiaPostHome.aspx
more info: https://en.wikipedia.org/wiki/India_Post"""
        ]
    },
    {
        "role": "model",
        "parts": [
            "Hello! 👋 I'm your friendly neighborhood postal assistant chatbot. How can I help you today?"
        ]
    }
])

@app.route("/")
def index():
    return render_template("index1.html")  # You must have 'templates/index1.html'

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({"error": "Bad Request: 'question' field is missing in the JSON data"}), 400

    user_input = data['question']
    try:
        response = chat_session.send_message(user_input)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
