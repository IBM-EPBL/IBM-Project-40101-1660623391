from flask import Flask , request , render_template , flash
import numpy as np
import os
import pandas as pd
from gevent.pywsgi  import WSGIServer
import utils

app= Flask(__name__, template_folder='templates', static_folder='static/css')
app.config.update(SECRET_KEY=os.urandom(24))
    



@app.route('/predict' , methods=['GET', 'POST'])
def predict():
    result = ""
    err = 0
    flightNumber = request.form.get("flightNumber")
    availableFlightNumbers = utils.getFlightNumbers()
    if int(flightNumber) not in availableFlightNumbers:
        err = 1
        return render_template('home.html', result = "Invalid Flight Number")
    date = request.form.get("date")
    formattedArray = utils.convertDateToFormat(date)
    month = formattedArray[0]
    dayOfMonth = formattedArray[1]
    dayOfWeek = formattedArray[2]
    origin = request.form.get("origin")
    if (origin == "ATL"):
        origin = 0
    elif (origin == "DTW"): 
        origin = 1
    elif (origin == "JFK"):
        origin = 2
    elif (origin == "MSP"):
        origin = 3
    elif (origin == "SEA"):
        origin = 4
    else:
        origin = 5
    if origin > 4 :
        err = 1
        return render_template('home.html', result = "Please enter a valid origin airport")
    dest = request.form.get("destination")

    if (dest == "ATL"):
        dest = 0
    elif (dest == "DTW"):
        dest = 1
    elif (dest == "JFK"):
        dest = 2
    elif (dest == "MSP"):
        dest = 3
    elif (dest == "SEA"):
        dest = 4
    else :
        dest = 5
    
    if dest > 4 :
        err = 1
        return render_template("home.html", result = "Please select a valid destination airport")
    
    depDelay = request.form.get("depDelay")
    if (depDelay == "yes"):
        depDelay = 1
    else:
        depDelay = 0
    scheduledArrivalTime = request.form.get("scheduledArrivalTime")
    scheduledArrivalTime = int(str(scheduledArrivalTime).split(":")[0])

    #Load the model
    print(flightNumber , month , dayOfMonth , dayOfWeek , origin , dest, scheduledArrivalTime, depDelay)
    if err == 0:
        result = utils.get_prediction(flightNumber , month , dayOfMonth , dayOfWeek , origin , dest, scheduledArrivalTime, depDelay)
        if (int(result) == 0):
            print("The Flight will be on time")
            msg = "The Flight will be on time"
        elif (int(result) == 1):
            print("The Flight will be delayed")
            msg = "The Flight will be delayed"
        return render_template('submit.html' , result = msg)



@app.route('/', methods=['POST' , 'GET'])
def home():
    return render_template('home.html')


# predict()
if (__name__ == '__main__'):
    
    app.run( debug = True , port = 5000)







    