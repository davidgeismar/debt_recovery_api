import sys, ast, getopt, types
import os
import math
#import pandas as pd
import numpy as np
import scipy as scipy
from scipy.optimize import curve_fit
import datetime as datetime
import time
from flask import Flask,jsonify,request
import json


app = Flask(__name__)

@app.route('/get-coefficients', methods=['POST'])
def main():
    #print(argv[0])
    string_params = request.values['data'].rstrip().replace('\n', '')
    array = string_params.split(',')
    new_array = []
    for i in array:
        new_array.append(float(i))
    return regression(new_array)

# MODELE DE FONCTION BASIQUE
def func(x, a, b):
    return a * (1 - np.exp(-b * x))

# MODELE DE FONCTION BASIQUE à double vitesse (marche pas très bien)
def func2(x, a, b, c, d):
    return a * (1 - np.exp(-b * x)) + c * (1 - np.exp(-d * x))

# MODELE DE FONCTION BASIQUE à difficultés croissantes
def func2v(x, a, b, c):
    return a * (1 - np.exp(-b * x - c * x * x))


def regression(versements_percent):
    #ydata = [0.0, 0.595, 1.02, 1.255, 1.445, 1.53, 1.60, 1.65, 1.7, 1.7, 1.7, 1.7, 1.7, 1.7]
    ydata = versements_percent
    xdata = np.arange(len(ydata))
    max_value = ydata[-1]

    popt2v, pcov = curve_fit(func2v, xdata, ydata, bounds=([max_value, 0, 0], [10000000, 10, 10]))
    y2v = func2v(xdata, popt2v[0], popt2v[1], popt2v[2])
    return jsonify(popt2v.tolist())

# if __name__ == "__main__":
#     main(sys.argv[1:])
if __name__ == '__main__':
    app.run(port=5000, debug=True)
