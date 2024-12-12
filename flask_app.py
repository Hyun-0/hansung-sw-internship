from flask import Flask, request, jsonify
from flask_data import data_handler
from flask_light_data import RGBLight

app = Flask(__name__)


# chat
@app.route('/request', methods=['POST'])
def send_request():
    data = request.get_json()
    response = data_handler.store_data(data)
    return jsonify(response), 200

@app.route('/response', methods=['GET'])
def get_response():
    data = data_handler.retrieve_response()
    return jsonify({"response": data}), 200

@app.route('/log', methods=['GET'])
def get_log():
    data = data_handler.retrieve_data()
    return jsonify(data), 200



# 기기제어
@app.route('/light/bedroom', methods=['GET'])
def get_bedroom_light():
    light = data_handler.get_bedroom_light()
    return jsonify({"light": light}), 200

@app.route('/light/living_room', methods=['GET'])
def get_livingroom_light():
    light = data_handler.get_livingroom_light()
    return jsonify({"light": light}), 200

@app.route('/light/kitchen', methods=['GET'])
def get_kitchen_light():
    light = data_handler.get_kitchen_light()
    return jsonify({"light": light}), 200

@app.route('/temperature', methods=['GET'])
def get_temperature():
    temperature = data_handler.get_temperature()
    return jsonify({"temperature": float(temperature)}), 200

@app.route('/humidity', methods=['GET'])
def get_humidity():
    humidity = data_handler.get_humidity()
    return jsonify({"humidity": float(humidity)}), 200



@app.route('/light/bedroom/change/<red>/<green>/<blue>', methods=['POST'])
def change_bedroom_light(red, green, blue):
    light = RGBLight(float(red), float(green), float(blue))
    changed_light = data_handler.change_bedroom_light(light)
    return jsonify({"bedroom": f"{changed_light}"}), 200

@app.route('/light/living_room/change/<red>/<green>/<blue>', methods=['POST'])
def change_livingroom_light(red, green, blue):
    light = RGBLight(float(red), float(green), float(blue))
    changed_light = data_handler.change_livingroom_light(light)
    return jsonify({"living_room": f"{changed_light}"}), 200

@app.route('/light/kitchen/change/<red>/<green>/<blue>', methods=['POST'])
def change_kitchen_light(red, green, blue):
    light = RGBLight(float(red), float(green), float(blue))
    changed_light = data_handler.change_kitchen_light(light)
    return jsonify({"kitchen": f"{changed_light}"}), 200

@app.route('/light/bedroom/change/power/<power>', methods=['POST'])
def change_bedroom_light_power(power):
    isLightOn = True if power == 'True' else False
    changed_light = data_handler.change_bedroom_light_status(isLightOn)
    return jsonify({"bedroom": f"{changed_light}"}), 200

@app.route('/light/living_room/change/power/<power>', methods=['POST'])
def change_livingroom_light_power(power):
    isLightOn = True if power == 'True' else False
    changed_light = data_handler.change_livingroom_light_status(isLightOn)
    return jsonify({"living_room": f"{changed_light}"}), 200

@app.route('/light/kitchen/change/power/<power>', methods=['POST'])
def change_kitchen_light_power(power):
    isLightOn = True if power == 'True' else False
    changed_light = data_handler.change_kitchen_light_status(isLightOn)
    return jsonify({"kitchen": f"{changed_light}"}), 200

@app.route('/temperature/change/<value>', methods=['POST'])
def change_temperature(value):
    valuee = float(value)
    data_handler.change_temperature(valuee)
    return jsonify({"temperature": f"{valuee}"}), 200

@app.route('/humidity/change/<value>', methods=['POST'])
def change_humidity(value):
    valuee = float(value)
    data_handler.change_humidity(valuee)
    return jsonify({"humidity": f"{valuee}"}), 200



@app.route('/temperature/add/<value>', methods=['POST'])
def add_temperature(value):
    valuee = float(value)
    data_handler.add_temperature(valuee)
    return jsonify({"temperature": f"{valuee}"}), 200

@app.route('/humidity/add/<value>', methods=['POST'])
def add_humidity(value):
    valuee = float(value)
    data_handler.add_humidity(valuee)
    return jsonify({"humidity": f"{valuee}"}), 200



@app.route('/temperature/sub/<value>', methods=['POST'])
def sub_temperature(value):
    valuee = float(value)
    data_handler.add_temperature(-valuee)
    return jsonify({"subtracted temperature": f"{valuee}"}), 200

@app.route('/humidity/sub/<value>', methods=['POST'])
def sub_humidity(value):
    valuee = float(value)
    data_handler.add_humidity(-valuee)
    return jsonify({"subtracted humidity": f"{valuee}"}), 200


# 실행
print(">> flask start")
app.run(host="0.0.0.0", port=1234, debug=False)