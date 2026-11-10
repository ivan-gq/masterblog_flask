from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # add code here to fetch the job posts from a file
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5500, debug=True)