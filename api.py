from flask import Flask, request, jsonify
from chatgui import chatgui
from keras.models import load_model

model = load_model('C:\Windows\System32\cmd.exe\chat_model.h5')


app = Flask(__name__)

@app.route('/chatgui', methods=['POST'])
def chatbot_api():
    data = request.get_json()
    message = data['message']
    response = chatgui(message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run()