from flask import Flask, send_file
import os

app = Flask(__name__)

# Ruta al favicon real (sin usar 'static')
FAVICON_PATH = os.path.join(os.path.dirname(__file__), 'favicon.ico')

@app.route('/')
def home():
    return '<h1>Welcome to My Flask App</h1>'

@app.route('/favicon.ico')
def favicon():
    return send_file(FAVICON_PATH, mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
