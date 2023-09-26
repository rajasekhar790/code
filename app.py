from flask import Flask, render_template, request, jsonify
from business_logic import get_weather  # Importing the function from business_logic.py

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message').lower()
    
    if "weather in" in user_message:
        city = user_message.split("in")[-1].strip()
        weather_data = get_weather(city)
        if weather_data:
            bot_response = f"The weather in {city} is {weather_data['description']} with a temperature of {weather_data['temp']}°C."
        else:
            bot_response = f"Sorry, I couldn't fetch the weather for {city}."
    else:
        bot_response = "I'm not sure how to respond to that."
    
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(debug=True)

