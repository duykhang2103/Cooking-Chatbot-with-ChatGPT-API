
from flask import Flask, render_template, request, jsonify
app = Flask(__name__, static_folder='public')
app.secret_key = "chatgpt"

from bot import *

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        input_text = request.form['input_text']
        output_text = main(input_text) # process_text is a function that returns the updated content f  or the div element
        return jsonify({'output_text': output_text})
    return render_template('layout.html')
