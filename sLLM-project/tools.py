from llama_index.core.tools import FunctionTool
from typing import List, Literal
from llama_index.core.bridge.pydantic import BaseModel, Field

import requests
import json

class Tools:
        def __init__(self):
                self.light_color_change_tool = FunctionTool.from_defaults(fn=change_light_color, fn_schema=ChangeLightColorArgs)
                self.light_power_change_tool = FunctionTool.from_defaults(fn=change_brightness, fn_schema=ChangeLightPowerArgs)
                self.temperature_change_tool = FunctionTool.from_defaults(fn=change_temperature, fn_schema=ChangeTempArgs)
                self.humidity_change_tool = FunctionTool.from_defaults(fn=change_humidity)
                
                self.temperature_add_tool = FunctionTool.from_defaults(fn=add_temperature)
                self.humidity_add_tool = FunctionTool.from_defaults(fn=add_humidity)
                
                self.temperature_sub_tool = FunctionTool.from_defaults(fn=sub_temperature)
                self.humidity_sub_tool = FunctionTool.from_defaults(fn=sub_humidity)
                
        def get_tools(self):
                return [
                        self.light_color_change_tool,
                        self.light_power_change_tool,
                        self.temperature_change_tool,
                        self.temperature_add_tool,
                        self.temperature_sub_tool,
                        self.humidity_change_tool,
                        self.humidity_add_tool,
                        self.humidity_sub_tool
                ]

from flask_light_data import RGBLight
# data_handler = DataHandler()

def change_light_color(position, red, green, blue):
        from flask_data import data_handler
        
        print(f'change {position}\'s color to RGB({red}, {green}, {blue})')
        
        light = RGBLight(float(red), float(green), float(blue))
        light.change_power(True)
        if ('kitchen' == position):
                changed_light = data_handler.change_kitchen_light(light)
        if ('bedroom' == position):
                changed_light = data_handler.change_bedroom_light(light)
        if ('living_room' == position):
                changed_light = data_handler.change_livingroom_light(light)
        return {f"{position}": f"{changed_light}"}

class ChangeLightColorArgs(BaseModel):
        position: Literal["bedroom", "living_room", "kitchen"] = Field(
                description="The rooms in house. Allowed values are: 'bedroom', 'living_room', 'kitchen'. You take a meal in kitchen, watch tv or use computer in living room, and take a sleep in bedroom."
        )
        red: float = Field(
                description="One of the color (RGB, Red) to be changed"
        )
        green: float = Field(
                description="One of the color (RGB, Green) to be changed"
        )
        blue: float = Field(
                description="One of the color (RGB, Blue) to be changed"
        )

def change_brightness(position, value: bool):
        from flask_data import data_handler
        
        print(f'change power to {value}')
        if ('kitchen' == position):
                changed_light = data_handler.change_kitchen_light_status(value)
        if ('bedroom' == position):
                changed_light = data_handler.change_bedroom_light_status(value)
        if ('living_room' == position):
                changed_light = data_handler.change_livingroom_light_status(value)
        return {f"{position}": f"{changed_light}"}

class ChangeLightPowerArgs(BaseModel):
        position: Literal["bedroom", "living_room", "kitchen"] = Field(
                description="The rooms in house. Allowed values are: 'bedroom', 'living_room', 'kitchen'. You take a meal in kitchen, watch tv or use computer in living room, and take a sleep in bedroom."
        )
        value: bool = Field(
                description="Power of the light. It will be 'True' when light turns on, and it will be 'False' when light turns off"
        )

def change_temperature(temperature):
        from flask_data import data_handler
        
        print(f'change temperature to {temperature}')
        response = data_handler.change_temperature(temperature)
        return {"changed temperature": f"{response}"}

class ChangeTempArgs(BaseModel):
        temperature: float = Field(
            description = "Input must be float type"
        )
        
        

def change_humidity(humidity):
        from flask_data import data_handler
        
        print(f'change temperature to {humidity}')
        response = data_handler.change_humidity(humidity)
        return {"changed temperature": f"{response}"}



def add_temperature(value):
        from flask_data import data_handler
        
        print(f'add {value} to temperature')
        data_handler.add_temperature(value)
        return {"added temperature": f"{value}"}

def add_humidity(value):
        from flask_data import data_handler
        
        print(f'add {value} to humidity')
        data_handler.add_humidity(value)
        return {"added humidity": f"{value}"}



def sub_temperature(value):
        from flask_data import data_handler
        
        print(f'subtract {value} to temperature')
        data_handler.add_temperature(-value)
        return {"subtracted temperature": f"{value}"}

def sub_humidity(value):
        from flask_data import data_handler
        
        print(f'subtract {value} to humidity')
        data_handler.add_humidity(-value)
        return {"subtracted temperature": f"{value}"}

# ---------- local intent ----------
def change_brightness_intent(position, value: bool):
    from flask_data import data_handler

    print(f'change power to {value}')
    if ('kitchen' == position):
        changed_light = data_handler.change_kitchen_light_status(value)
    if ('bedroom' == position):
        changed_light = data_handler.change_bedroom_light_status(value)
    if ('living_room' == position): 
        changed_light = data_handler.change_livingroom_light_status(value)

    position_name = get_position_name(position)
    
    return  f"{position_name}의 조명을 켰습니다" if value else f"{position_name}의 조명을 껐습니다"

def change_temperature_intent(temperature):
    from flask_data import data_handler
    
    print(f'change temperature to {temperature}')
    response = data_handler.change_temperature(float(temperature))


    return f"실내 목표 온도를 {response}도로 설정하였습니다."

def change_humidity_intent(humidity):
        from flask_data import data_handler
        
        print(f'change temperature to {humidity}')
        response = data_handler.change_humidity(float(humidity))
        return f"실내 목표 습도를 {response}도로 설정하였습니다."


def add_temperature_intent(value):
    from flask_data import data_handler
    
    print(f'add {value} to temperature')
    data_handler.add_temperature(float(value))
    return f"실내 목표 온도를 {value}도 올렸습니다."

def add_humidity_intent(value):
        from flask_data import data_handler
        
        print(f'add {value} to humidity')
        data_handler.add_humidity(float(value))
        return f"실내 목표 습도를 {value}도 높였습니다."

def sub_temperature_intent(value):
        from flask_data import data_handler
        
        print(f'subtract {value} to temperature')
        data_handler.add_temperature(-float(value))
        return f"실내 목표 온도를 {value}도 낮췄습니다."

def sub_humidity_intent(value):
        from flask_data import data_handler
        
        print(f'subtract {value} to humidity')
        data_handler.add_humidity(-float(value))
        return f"실내 목표 습도를 {value}도 낮췄습니다."


    

def get_position_name(position):
    if position == "kitchen" :
        return "주방"

    elif position == "bedroom" :
        return "침실"

    elif position == "living_room" :
        return "거실"







# ----------------- 감정분석 ------------------
import re
import pickle
import numpy as np
import MeCab

from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences

import tensorflow as tf
gpus = tf.config.list_physical_devices('GPU')
if gpus:
  # 텐서플로가 첫 번째 GPU에 1GB 메모리만 할당하도록 제한
  try:
    tf.config.set_logical_device_configuration(
        gpus[0],
        [tf.config.LogicalDeviceConfiguration(memory_limit=8192)])
  except RuntimeError as e:
    # 프로그램 시작시에 가상 장치가 설정되어야만 합니다
    print(e)

print("loading sentiment model...")
mecab = MeCab.Tagger()
stopwords = ['도', '는', '다', '의', '가', '이', '은', '한', '에', '하', '고', '을', '를', '인', '듯', '과', '와', '네', '들', '듯', '지', '임', '게']

with open('old_sentiment/tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

loaded_model = load_model('old_sentiment/best_model.keras')
max_len = 30

def sentiment_predict(new_sentence):
  new_sentence = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]','', new_sentence)
  new_sentence = mecab.parse(new_sentence)
  new_sentence = [word for word in new_sentence if not word in stopwords]
  encoded = tokenizer.texts_to_sequences([new_sentence])
  pad_new = pad_sequences(encoded, maxlen = max_len)
  output = loaded_model.predict(pad_new)
  score = float(output[0])
  
  if(score > 0.6):
    print("{:.2f}% 확률로 긍정입니다.".format(score * 100))
  else:
    print("{:.2f}% 확률로 부정입니다.".format((1 - score) * 100))

  return score