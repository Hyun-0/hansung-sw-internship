import re
import pickle
import numpy as np
import MeCab

from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences

print("loading sentiment model...")
mecab = MeCab.Tagger()
stopwords = ['도', '는', '다', '의', '가', '이', '은', '한', '에', '하', '고', '을', '를', '인', '듯', '과', '와', '네', '들', '듯', '지', '임', '게']

with open('tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

loaded_model = load_model('best_model.keras')
max_len = 30

def sentiment_predict(new_sentence):
  new_sentence = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]','', new_sentence)
  new_sentence = mecab.parse(new_sentence)
  new_sentence = [word for word in new_sentence if not word in stopwords]
  encoded = tokenizer.texts_to_sequences([new_sentence])
  pad_new = pad_sequences(encoded, maxlen = max_len)

  score = float(loaded_model.predict(pad_new))
  
  if(score > 0.6):
    print("{:.2f}% 확률로 긍정입니다.".format(score * 100))
  else:
    print("{:.2f}% 확률로 부정입니다.".format((1 - score) * 100))

  return score