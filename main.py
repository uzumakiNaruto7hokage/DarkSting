import os
from flask import Flask, jsonify, request, render_template
from types import MethodType
import json

from werkzeug.wrappers import response

app = Flask(__name__)

os.chdir("static/buffer")


@app.route('/')
def index():
    return render_template("broadcast.html")

@app.route('/clearBuffer', methods=["POST"])
def clearBuffer():
    data = request.get_json()
    with open(f"buffer_{data['deviceId']}.json", "w") as file:
        file.write("{}")
    return jsonify({"status": "buffer cleared"})


@app.route('/getProcess', methods=["POST"])
def getProcess():
    data = request.get_json()
    id = data["processID"]
    with open(f"buffer_{data['deviceId']}.json", 'r') as file:
        content = json.load(file)
    if len(content) == 0 or len(content) < int(id):
        return jsonify({"process":"empty"})
    else:
        return jsonify({"process": content[data['processID']]})
        # return jsonify({"process":"empty"})

@app.route('/broadcast', methods=["POST"])
def broadcast():
    data = request.get_json()
    type = data['type']
    code = data["code"]
    repeating = data['repeating']
    for i in os.listdir():
        content = {}
        with open(i, 'r') as file:
            content = json.load(file)
        id = str(len(content)+1)
        with open(i, 'w') as file:
            content[id] = {
                "type": type,
                "code": code,
                "reapeating": repeating,
                "compiled": False,
                "nodeResponse": ""
            }
            json.dump(content, file)
    return jsonify({"status": "sucess"})

@app.route("/submitResponse", methods=["POST"])
def submitResponse():
    data = request.get_json()
    processId = data["processID"]
    r = data["response"]
    with open(f"buffer_{data['deviceId']}.json", 'r') as file:
        content = json.load(file)
        content[processId]["nodeResponse"] = r
        content[processId]["compiled"] = True
        
    with open(f"buffer_{data['deviceId']}.json", 'w') as file:
        json.dump(content, file)
        
    return jsonify({"status": "succsess"})

@app.route("/collectOutput")
def collectOutput():
    output = []
    for i in os.listdir():
        with open(i, 'r') as file:
            content = json.load(file)
            index = str(len(content))
            s = content[index]["nodeResponse"]
            if s != "":
                output.append(s)
    
    # print(output)
    return jsonify({
        "output":output
    })
@app.route("/executeOnServer",methods=["POST"])
def executeOnServer():
    pass
if __name__ == '__main__':
    app.run(host="0.0.0.0")
