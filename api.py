import flask
import logging
import json
from flask import request, jsonify,g,render_template, url_for,session
from random import randint
import time
from datetime import datetime

flaskLogger = logging.getLogger('werkzeug')
flaskLogger.setLevel(logging.ERROR)

logging.basicConfig(filename='datalog.log', encoding='utf-8', level=logging.INFO,format='%(message)s')

app = flask.Flask(__name__)
app.config["DEBUG"] = True

data = json.load(open("data.json"))

def write_json(data, filename='data.json'): 
    with open(filename,'w') as file: 
        json.dump(data, file, indent=4) 

def logApiCall(message,startTime):
    timeStamp = time.time()
    difString = "%.3f" % (timeStamp - startTime)

    logging.info(message +", "+ difString +", "+ str(int(timeStamp)))

@app.route('/', methods=['GET'])
def home():
    return "<h1>Kartaca API</h1><p>This site is a prototype API</p>"

@app.route('/api/data/all', methods=['GET'])
def api_all():
    request_start_time = time.time()
    time.sleep(randint(0,3))

    logApiCall("GET", request_start_time)

    return jsonify(data)

@app.route('/api/data/<int:data_id>', methods=['GET'])
def api_filter(data_id):
    request_start_time = time.time()
    time.sleep(randint(0,3))

    result = None
    
    for people in data['data']:
        if people['id'] == data_id:
            result = people

    logApiCall("GET", request_start_time)

    return jsonify(result)

@app.route('/api/data', methods=['POST'])
def api_post():
    request_start_time = time.time()
    time.sleep(randint(0,3))
    if not request.json:
        return "Please enter a Name." 
    
    post_request = { "id": data['lastId'], 
    "name": request.json['name'], 
    "country": request.json.get('country',"")}

    data['lastId']+=1
    temp=data['data']
    temp.append(post_request)

    write_json(data)

    logApiCall("POST", request_start_time)

    return {"success":True,"error":None, "data":post_request}

@app.route('/api/data', methods=['DELETE'])
def api_delete():
    request_start_time = time.time()
    time.sleep(randint(0,3))

    if not request.json or not 'id' in request.json:
        return "Please enter an id."
    delete_request = { "id": request.json['id'], 
    "name": request.json['name'], 
    "country": request.json.get('country',"")}


    temp=data['data']
    temp.remove(delete_request)
    write_json(data)

    logApiCall("DELETE", request_start_time)
    
    return {"success":True,"error":None, "data":delete_request}

@app.route('/api/data/<int:data_id>', methods=['PUT'])
def api_put(data_id):
    request_start_time = time.time()
    time.sleep(randint(0,3))
    if not request.json:
        return "Please enter a Name." 
    
    done = False

    put_request = {"name": request.json['name'],
    "country": request.json.get('country',"")}

    for people in data['data']:
        if people['id'] == data_id:
            people['name'] = put_request['name']
            people['country'] = put_request['country']
            done = True
    
    if done == False:
        return "Error! Id not found"

    write_json(data)
    logApiCall("PUT", request_start_time)        

    return {"success":True,"error":None, "data":people}

@app.route('/api/log', methods=['GET'])
def get_logs():
    logs = {
        "get":[],
        "post":[],
        "put":[],
        "delete":[]
    }

    with open("datalog.log",'r') as file: 
        lines = file.readlines()
        for line in lines:
            splited = line.split(", ")
            method = splited[0]
            time = datetime.fromtimestamp(int(splited[2]))
            details = {"x":time.strftime("%d.%m.%Y %H:%M:%S"),"y":splited[1]}
            if method == "GET":
                logs["get"].append(details)
            elif method == "POST":
                logs["post"].append(details)
            elif method == "PUT":
                logs["put"].append(details)
            elif method == "DELETE":
                logs["delete"].append(details)      
    return jsonify(logs)

@app.route('/api/dashboard')
def chart():
    
    return render_template('chart.html')

app.run()
