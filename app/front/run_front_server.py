import json
import urllib
import numpy as np

from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from requests.exceptions import ConnectionError
from wtforms import IntegerField, SelectField, StringField
from wtforms.validators import DataRequired


class ClientDataForm(FlaskForm):
    ph = StringField('ph', validators=[DataRequired()])
    hardness = StringField('Hardness', validators=[DataRequired()])
    solids = StringField('Solids', validators=[DataRequired()])
    chloramines = StringField('Chloramines', validators=[DataRequired()])
    sulfate = StringField('Sulfate', validators=[DataRequired()])


app = Flask(__name__)
app.config.update(
    CSRF_ENABLED=True,
    SECRET_KEY='you-will-never-guess',
)


def get_prediction(x):
    ph, hardness, solids, chloramines, sulfate = x
    body = {'ph': ph, 'Hardness': hardness, 'Solids': solids,
            'Chloramines': chloramines, 'Sulfate': sulfate}

    myurl = 'http://localhost:8180/predict'
    req = urllib.request.Request(myurl)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')
    req.add_header('Content-Length', len(jsondataasbytes))
    response = urllib.request.urlopen(req, jsondataasbytes)

    return json.loads(response.read())['predictions']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predicted/<response>')
def predicted(response):
    response = json.loads(response)
    print(response)
    return render_template('predicted.html', response=response)


@app.route('/predict_form', methods=['GET', 'POST'])
def predict_form():
    form = ClientDataForm()
    data = dict()
    if request.method == 'POST':
        data['ph'] = request.form.get('ph')
        data['Hardness'] = request.form.get('hardness')
        data['Solids'] = request.form.get('solids')
        data['Chloramines'] = request.form.get('chloramines')
        data['Sulfate'] = request.form.get('sulfate')

        try:
            response = str(get_prediction((data['ph'],
                                           data['Hardness'],
                                           data['Solids'],
                                           data['Chloramines'],
                                           data['Sulfate']
                                           )))
            print(response)
        except ConnectionError:
            response = json.dumps({"error": "ConnectionError"})
        return redirect(url_for('predicted', response=response))
    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8181, debug=True)
