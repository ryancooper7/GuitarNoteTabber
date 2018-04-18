import math
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/<string:index>/', methods=['GET','POST'])
def my_form_post(index):
    if request.method == 'POST':
        print len(request.data)
        return request.data
    else:
        return render_template('%s.html' % index)

if __name__ == "__main__":
    app.run(debug=True)