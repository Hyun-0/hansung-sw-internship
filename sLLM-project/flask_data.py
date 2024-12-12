from flask_light_data import RGBLight
from my_llm import MyLLM

class DataHandler:
    def __init__(self):
        self.agent = MyLLM()
        self.data_store = []
        self.current_response = ""
        
        # raspberry pi에서 데이터 받아올 예정
        self.bedroom_light = RGBLight()
        self.livingroom_light = RGBLight()
        self.kitchen_light = RGBLight()
        self.temperature = 20
        self.humidity = 30

    def store_data(self, data):
        request = data["request"]

        llm = MyLLM()
        response = llm.chat(request)
         
        self.current_response = f"{response}"
        store = {
                "request": f"{request}",
                "response": f"{response}"
        }
        self.data_store.append(store)
        return store

    def retrieve_response(self):
        return self.current_response
    
    def retrieve_data(self):
        return self.data_store
    
    def get_bedroom_light(self):
        return self.bedroom_light.to_json()
    
    def get_livingroom_light(self):
        return self.livingroom_light.to_json()
    
    def get_kitchen_light(self):
        return self.kitchen_light.to_json()
    
    def get_temperature(self):
        return self.temperature
    
    def get_humidity(self):
        return self.humidity
 
    # 여기서부터 function call로 실행 예정   
    def change_bedroom_light(self, light: RGBLight):
        self.bedroom_light.change_color(light)
        return self.bedroom_light.to_json()
    
    def change_livingroom_light(self, light: RGBLight):
        self.livingroom_light.change_color(light)
        return self.livingroom_light.to_json()
    
    def change_kitchen_light(self, light: RGBLight):
        self.kitchen_light.change_color(light)
        return self.kitchen_light.to_json()
    
    def change_bedroom_light_status(self, isLightOn):
        self.bedroom_light.change_power(isLightOn)
        return self.bedroom_light.to_json()
    
    def change_livingroom_light_status(self, isLightOn):
        self.livingroom_light.change_power(isLightOn)
        return self.livingroom_light.to_json()
    
    def change_kitchen_light_status(self, isLightOn):
        self.kitchen_light.change_power(isLightOn)
        return self.kitchen_light.to_json()
    
    def change_temperature(self, temperature):
        self.temperature = temperature
        return self.temperature
    
    def change_humidity(self, humidity):
        self.humidity = humidity
        return self.humidity
    
    def add_bedroom_light_power(self, fix_value):
        self.bedroom_light.power += fix_value
        if (self.bedroom_light.power < 0):
            self.bedroom_light.power = 0
        elif (self.bedroom_light.power > 100):
            self.bedroom_light.power = 100
        return self.bedroom_light.to_json()
    
    def add_livingroom_light_power(self, fix_value):
        self.livingroom_light.power += fix_value
        if (self.livingroom_light.power < 0):
            self.livingroom_light.power = 0
        elif (self.livingroom_light.power > 100):
            self.livingroom_light.power = 100
        return self.livingroom_light.to_json()
    
    def add_kitchen_light_power(self, fix_value):
        self.kitchen_light.power += fix_value
        if (self.kitchen_light.power < 0):
            self.kitchen_light.power = 0
        elif (self.kitchen_light.power > 100):
            self.kitchen_light.power = 100
        return self.kitchen_light.to_json()
    
    def add_temperature(self, fix_value):
        self.temperature += fix_value
        return self.temperature
    
    def add_humidity(self, fix_value):
        self.humidity += fix_value
        return self.humidity

data_handler = DataHandler()