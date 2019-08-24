from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

sensorData = {"sensor": "FC28", "variable": "Humedad de la tierra", "unidades": "%"}

dataCapture = [
  {"fecha": "2019-08-13 11:04:03", **sensorData, "valor": 38},
  {"fecha": "2019-06-22 14:24:01", **sensorData, "valor": 35},
  {"fecha": "2019-08-21 22:04:59", **sensorData, "valor": 31},
  {"fecha": "2019-05-03 05:23:15", **sensorData, "valor": 24},
  {"fecha": "2019-08-15 17:12:30", **sensorData, "valor": 18},
  {"fecha": "2019-08-22 11:04:03", **sensorData, "valor": 35},
  {"fecha": "2019-08-13 14:24:01", **sensorData, "valor": 18},
  {"fecha": "2019-06-22 22:04:59", **sensorData, "valor": 21},
  {"fecha": "2019-07-25 05:23:15", **sensorData, "valor": 18},
  {"fecha": "2019-06-08 17:12:30", **sensorData, "valor": 35}
]

@app.route("/")
def getBasico():
  return sensorData

@app.route("/data", methods = ['GET'])
def getAll():
  return jsonify(dataCapture)

@app.route("/data/mode")
def getModa():
  values = []
  for m in dataCapture :
    values.append(m['valor'])
  
  mostCommon = []
  higher = values.count(values[0])
  for i in values :
    current = values.count(i)
    if current > higher :
      higher = current
      mostCommon.clear()  
      mostCommon.append(i)
    elif current == higher :
      if i not in mostCommon :
        mostCommon.append(i)

  return jsonify(mostCommon)

@app.route("/data", methods=['POST'])
def postV():
  now = datetime.now()
  body = request.json
  body['fecha'] = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
  dataCapture.append({**body, **sensorData})
  return jsonify(dataCapture)

@app.route("/data/<string:fecha>", methods=['DELETE'])
def deleteV(fecha):
  found = False
  for m in dataCapture :
    if fecha == m['fecha'][:10] :
      found = True
      dataCapture.remove(m)
  return 'Borrado con éxito.' if found else 'Elemento no encontrado.'

@app.route("/data/<string:fecha>", methods=['PUT'])
def putV(fecha):
  found = False
  for m in dataCapture :
    if fecha == m['fecha'][:10] :
      found = True
      m['valor'] = 1
  return 'Actualizado.\nSe cambió el valor a 1.' if found else 'Elemento no encontrado.'

app.run(port=5000, debug=True)