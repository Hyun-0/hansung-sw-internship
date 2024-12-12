from tools import *
from enum import Enum, unique
from EntityRecognizer import EntityRecognizer
from IntentClassifier import IntentClassifier
from hugging import HuggingFaceNotebookLogin
from config import SYSTEM_PROMPT, QUERY_WRAPPER_PROMPT
from main import *

@unique
class FunctionIndex(Enum):
    SWITCH_KITCHEN_LIGHT_ON         = 0
    SWITCH_KITCHEN_LIGHT_OFF        = 1
    SWITCH_BEDROOM_LIGHT_ON         = 2
    SWITCH_BEDROOM_LIGHT_OFF        = 3
    SWITCH_LIVING_ROOM_LIGHT_ON     = 4
    SWITCH_LIVING_ROOM_LIGHT_OFF    = 5
    
    CHANGE_TEMPERATURE              = 6
    ADD_TEMPERATURE                 = 7
    SUB_TEMPERATURE                 = 8
    CHANGE_HUMIDITY                 = 9
    ADD_HUMIDITY                    = 10
    SUB_HUMIDITY                    = 11

    SWITCH_LIGHT_COLOR = 12
    AAAA = 13
    # Rag 안쓰는 감정 분석 추가



class MyLLM:
    def __init__(self):
        self.huggingface_login = HuggingFaceNotebookLogin()
        self.huggingface_login.login()
        self.intent_classifier = IntentClassifier()
        self.entity_recognizer = EntityRecognizer()
        
        
        
        return
    
    def chat(self, request):
        # request intent classification
        print(f"request : {request}")
        predict_intent, probability = self.intent_classifier.predict(request)
        
        # test code
        print(f"intent class : {predict_intent}")
        print(f"probability: {probability}")
        print(max(probability[0]))

        if max(probability[0]) < 0.98 :

            prompt_message = f"{request} 라는 사용자의 입력에 대해 '긍정', '중립', '부정' 으로만 답변 해줘."
            response = openai_request(request)
            print("dfadwsjfadsfhioasdfjaewklfjeawla response")
            print(response)
            # # 감정분석
            # # ----------- positive -------------
            # score = sentiment_predict(request)
            # print(f"sentimental score: {score}")
            if (f'{response}' == '긍정'):
                # 긍정

                response = agent.chat(request)
                print(response.sources)
                return response

                
                # # 하얀색 제일 밝게 (255, 255, 255)
                # # response 값 리턴
                # print(f"감정분석! 긍정 : {score}")
                # return "긍정 ㅠㅠ.."

            elif (f'{response}' == '부정'):
                # 부정
                response = agent.chat(request)
                print(response.sources)
                return response
                
                # # 주황 빛 나는 (조도 낮게) (255, 178, 102) (조도는 전체적으로 rgb 값 낮춰주기)
                # # 25도 정도
                # # response 값 리턴
                # print(f"감정분석! 부정 : {score}")
                # return "부정 ㅠㅠ.."

            else :
                # rag
                print("------- rag output -------")
                answer = get_llm_output(request)
                print(answer)
                return answer


        # 조명 조도 10 낮춰줘
        entity = self.entity_recognizer.getIntValueInString(request)
        # # entity extraction
        # entity = {
        #     "red": 100, "green":100, "blue": 100, "isLightOn": True,
        #     "temperature": 10, "fix_temperature": 5,
        #     "humidity": 10, "fix_humidity": 5
        # }
        
        if (predict_intent >= FunctionIndex.SWITCH_KITCHEN_LIGHT_ON.value and predict_intent <= FunctionIndex.AAAA.value):

            # if len(entity) != 1 :
            #         # chatgpt 사용 예정
            #         print(f"entity.count: {len(entity)}")
            #         print(f"entity: {entity}")
            #         result = agent.chat(request)

            a = FunctionIndex.CHANGE_TEMPERATURE.value < predict_intent < FunctionIndex.SUB_HUMIDITY.value
            
            if len(entity) < 1 and a:
                response = agent.chat(request)
                return response
        
            if predict_intent == FunctionIndex.SWITCH_KITCHEN_LIGHT_ON.value:
                result = change_brightness_intent("kitchen", True)
            elif predict_intent == FunctionIndex.SWITCH_KITCHEN_LIGHT_OFF.value:
                result = change_brightness_intent("kitchen", False)

            elif predict_intent == FunctionIndex.SWITCH_BEDROOM_LIGHT_ON.value:
                result = change_brightness_intent("bedroom", True)
            elif predict_intent == FunctionIndex.SWITCH_BEDROOM_LIGHT_OFF.value:
                result = change_brightness_intent("bedroom", False)
                
            elif predict_intent == FunctionIndex.SWITCH_LIVING_ROOM_LIGHT_ON.value:
                result = change_brightness_intent("living_room", True)
            elif predict_intent == FunctionIndex.SWITCH_LIVING_ROOM_LIGHT_OFF.value:
                result = change_brightness_intent("living_room", False)
            
            elif predict_intent == FunctionIndex.CHANGE_TEMPERATURE.value:
                result = change_temperature_intent(int(entity[0]))
            elif predict_intent == FunctionIndex.ADD_TEMPERATURE.value:
                result = add_temperature_intent(int(entity[0]))
            elif predict_intent == FunctionIndex.SUB_TEMPERATURE.value:
                result = sub_temperature_intent(int(entity[0]))
                
            elif predict_intent == FunctionIndex.CHANGE_HUMIDITY.value:
                result = change_humidity_intent(int(entity[0]))
            elif predict_intent == FunctionIndex.ADD_HUMIDITY.value:
                result = add_humidity_intent(int(entity[0]))
            elif predict_intent == FunctionIndex.SUB_HUMIDITY.value:
                result = sub_humidity_intent(int(entity[0]))

            elif predict_intent == FunctionIndex.SWITCH_LIGHT_COLOR.value or FunctionIndex.AAAA.value :
                response = agent.chat(request)
                return response
                

        
        return result

def get_llm_output(request) :
    # example - request: "주방 조명 10 낮춰줘"
    output = query_engine.query(request)
    print(output)
    return output



# openai
import openai

# 발급 api key
OPENAI_API_KEY = "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"

# key 인증
openai.api_key = OPENAI_API_KEY

from openai import OpenAI
import pandas as pd

client = OpenAI(
    api_key = OPENAI_API_KEY
)

def openai_request(request) :
    request_query = client.chat.completions.create(
        messages=[
            {"role": "user", "content": f"{request}에 대한 답변으로 감정을 분석해서 무조건 '긍정', '중립', '부정' 단어로만 답 해"}
        ], model="gpt-4o"
    )
    
    answer = request_query.choices[0].message.content
    return answer