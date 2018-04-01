from flask import Flask, render_template

app = Flask(__name__)

@app.route('/<string:index>/')
def render_static(index):
    return render_template('%s.html' % index)


if __name__ == "__main__":
    app.run(debug=True)