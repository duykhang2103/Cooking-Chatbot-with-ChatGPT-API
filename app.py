
from flask import Flask, render_template, request, flash, jsonify
app = Flask(__name__, static_folder='public')
app.secret_key = "chatgpt"

from bot import * # bot_file is the name of the file you implement your chatbot

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        input_text = request.form['input_text']
        output_text = main(input_text) # process_text is a function that returns the answer of the chatbot
        return jsonify({'output_text': output_text})
    return render_template('layout.html')

