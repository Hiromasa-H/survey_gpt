from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import openai 
import arxiv

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)