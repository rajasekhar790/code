from flask import Flask, render_template, request, jsonify
from business_logic import ChatBotLogic

app = Flask(__name__)
chatbot = ChatBotLogic()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = chatbot.get_response(user_input)
    return jsonify(response=response)

if __name__ == '__main__':
    app.run(debug=True)
