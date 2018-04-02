import math
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/<string:index>/')
def render_static(index):
    return render_template('%s.html' % index)

@app.route('/<string:index>/', methods=['POST'])
def my_form_post(index):
    text = float(request.form['text'])
    processed_text = str(math.sqrt(text))
    return render_template('%s.html' % index, text=processed_text)


if __name__ == "__main__":
    app.run(debug=True)