import pandas as pd
from pyfasttext import FastText

train = pd.read_csv("/home/ubuntu/Django/fasttext/kakao - Question.csv")
train['label'] = train['label'].astype(str)
train['fast'] = "__label__" + train['label'] + " " + train['text']
print(train.head(1))

train['fast'].to_csv('fast.txt', index=False, header=None)

model = FastText()
model.supervised(input="fast.txt", output='train', epoch=100, lr=0.7)
model.supervised(input="fast.txt", output='/home/ubuntu/Django/app/train', epoch=100, lr=0.7)

print(model.nlabels)
print("모델 생성, train.bin")

print("ex")
print("model.predict_proba_single('반가워', k=5)")
print("[('2', 0.9960937499035479), ('1', 0.0019531445243914027)]")
