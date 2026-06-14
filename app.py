from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Running on port 5000 with debug enabled
    app.run(debug=True, port=5000)
