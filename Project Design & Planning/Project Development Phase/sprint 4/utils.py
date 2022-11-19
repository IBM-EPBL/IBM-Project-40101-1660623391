from datetime import datetime
import requests
import pandas as pd

def convertDateToFormat(date):
    date = datetime.strptime(date, '%Y-%m-%d')
    dayofWeek = date.weekday()
    month=date.month
    dayOfMonth=date.day

    return [month, dayOfMonth, dayofWeek]


def getFlightNumbers():
    df = pd.read_csv("flightdata.csv")
    flightNumbers = df['FL_NUM'].unique()
    return flightNumbers
    
def get_prediction(flightNumber = 39, month =12 , dayofMonth = 9, dayofWeek = 5 , origin = 1 , dest = 3, scheduledArrivalTime = 12, depDelay = 0 ):
    values = [[flightNumber, month, dayofMonth, dayofWeek, origin, dest, scheduledArrivalTime, depDelay]]

    
    # NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
    API_KEY = "kr_VNpRFqz0Mte9mcgQLk25-SFN2SevdqscISORzvMzj"
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]

    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"field": ["FL_NUM","MONTH","DAY_OF_MONTH","DAY_OF_WEEK","ORIGIN","DEST","CRS_ARR_TIME","DEP_DEL15","ARR_DEL15"], "values": values}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/d68c1881-d3af-408c-a068-e97db487099a/predictions?version=2022-11-04', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    
    predictionResult = response_scoring.json()
    print(predictionResult)
    result = predictionResult["predictions"][0]["values"][0][0]

    return result 

getFlightNumbers()
