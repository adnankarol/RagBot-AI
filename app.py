__author__ = "Adnan Karol"
__version__ = "1.0.0"
__maintainer__ = "Adnan Karol"
__email__ = "adnanmushtaq5@gmail.com"


# Import Dependencies
from flask import Flask, request, jsonify, render_template
from RagBot import Chatbot, KnowledgeBase
from flask_cors import CORS


app = Flask(__name__)
# Enable CORS for all routes
CORS(app)

# Initialize the knowledge base and chatbot
knowledge_base = KnowledgeBase(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    file_path="Internal_Data.txt",
)
chatbot = Chatbot(model_name="llama3", knowledge_base=knowledge_base)


# Serving the index.html when accessing the root URL
@app.route("/")
def index():
    return render_template("index.html")


# Route to handle chat requests
@app.route("/chat/", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("question")
    context = data.get("context", "")

    # Generate the response based on the user input
    response = chatbot.handle_input(user_input)
    return jsonify({"answer": response})


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8000)
