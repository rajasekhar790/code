from flask import Flask, render_template, request, jsonify
from business_logic import ChatBotLogic

app = Flask(__name__)

# Initialize the ChatBotLogic class
chatbot = ChatBotLogic('data.xlsx')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message').lower()
    
    # Get response from the chatbot logic
    bot_response = chatbot.get_response(user_message)
    
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(debug=True)
