import pandas as pd
import numpy as np
import os
import flask
import logging
from logging.handlers import RotatingFileHandler
from time import strftime
import dill
dill._dill._reverse_typemap['ClassType'] = type

# initialize our Flask application and the model
app = flask.Flask(__name__)
model = None

handler = RotatingFileHandler(filename='app.log', maxBytes=100000, backupCount=10)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def load_model(model_path):
    # load the pre-trained model
    global model
    with open(model_path, 'rb') as f:
        model = dill.load(f)
    print(model)


modelpath = "models/rf_pipeline.dill"
load_model(modelpath)


@app.route("/", methods=["GET"])
def general():
    return """Welcome to potability prediction process. Please use 'http://<address>/predict' to POST"""


@app.route("/predict", methods=["POST"])
def predict():
    # initialize the data dictionary that will be returned from the
    # view
    data = {"success": False}
    dt = strftime("[%Y-%b-%d %H:%M:%S]")
    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":

        ph, hardness, solids, chloramines, sulfate = '', '', '', '', ''

        if len(ph) == 0:
            ph = np.nan

        if len(hardness) == 0:
            hardness = np.nan

        if len(solids) == 0:
            solids = np.nan

        if len(chloramines) == 0:
            chloramines = np.nan

        if len(sulfate) == 0:
            sulfate = np.nan

        request_json = flask.request.get_json()

        if request_json["ph"]:
            ph = request_json['ph']
            if type(ph) is str:
                if ph.lstrip('-').replace('.', '', 1).isdigit() is False:
                    ph = np.nan

        if request_json["Hardness"]:
            hardness = request_json['Hardness']
            if type(hardness) is str:
                if hardness.lstrip('-').replace('.', '', 1).isdigit() is False:
                    hardness = np.nan

        if request_json["Solids"]:
            solids = request_json['Solids']
            if type(solids) is str:
                if solids.lstrip('-').replace('.', '', 1).isdigit() is False:
                    solids = np.nan

        if request_json["Chloramines"]:
            chloramines = request_json['Chloramines']
            if type(chloramines) is str:
                if chloramines.lstrip('-').replace('.', '', 1).isdigit() is False:
                    chloramines = np.nan

        if request_json["Sulfate"]:
            sulfate = request_json['Sulfate']
            if type(sulfate) is str:
                if sulfate.lstrip('-').replace('.', '', 1).isdigit() is False:
                    sulfate = np.nan

        logger.info(
            f'{dt} Data: ph={ph}, Hardness={hardness}, Solids={solids}, Chloramines={chloramines}, Sulfate={sulfate}')
        try:
            preds = model.predict_proba(pd.DataFrame({"ph": [ph],
                                                      "Hardness": [hardness],
                                                      "Solids": [solids],
                                                      "Chloramines": [chloramines],
                                                      "Sulfate": [sulfate]
                                                      }))
        except AttributeError as e:
            logger.warning(f'{dt} Exception: {str(e)}')
            data['predictions'] = str(e)
            data['success'] = False
            return flask.jsonify(data)

        data["predictions"] = preds[:, 1][0]
        # indicate that the request was a success
        data["success"] = True

    # return the data dictionary as a JSON response
    return flask.jsonify(data)


# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
    print(("* Loading the model and Flask starting server..."
           "please wait until server has fully started"))
    port = int(os.environ.get('PORT', 8180))
    app.run(host='0.0.0.0', debug=True, port=port)
