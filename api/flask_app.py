import subprocess
import webbrowser

import numpy as np
from flask_cors import CORS
from flask import Flask, request, jsonify, render_template
import genetic_code_main
from other import Print
from Data import *
import waitress


@app.route("/build", methods=['POST'])
def build():
    POSTdata = request.json

    A = []
    B = []
    capacity = POSTdata['capacity']
    costs_table = []
    for i in POSTdata['storeCount']:
        A.append(int(i))
    for i in POSTdata['destinationCount']:
        B.append(int(i))

    if type(POSTdata['distances'][0]) == dict:
        costs_table = [[None for _ in range(len(B))] for _ in range(len(A))]
        for distance in POSTdata['distances']:
            costs_table[distance['store']][distance['destination']] = distance['length']

    if type(POSTdata['distances'][0]) == list:
        costs_table = POSTdata['distances']

    if "distanceBetweenDestinations" in POSTdata:
        distance_between_destinations = POSTdata["distanceBetweenDestinations"]
        Print(distance_between_destinations)
        data = Data(A, B, costs_table,capacity,distance_between_destinations)
    else:
        data = Data(A,B,costs_table,capacity)



    result = genetic_code_main.Start(data)
    rows, columns = data.giveWithoutExcess()
    result_copy = np.copy(result)
    distribution = result_copy[:len(rows),:len(columns)].tolist()
    response = {"distribution":distribution,"ways":result.ways}

    return jsonify(response)

def application():
    host = "localhost"
    port = "5000"
    url = f'http://{host}:{port}'
    waitress.serve(app, host=host, port=port)
