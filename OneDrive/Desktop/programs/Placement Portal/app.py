
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
    jobs=[{'title':'Python Developer'},{'title':'Data Analyst'}]
    return render_template('index.html', jobs=jobs)

if __name__ == '__main__':
    app.run(debug=True)
