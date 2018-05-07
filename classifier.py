from pyfasttext import FastText
import pandas as pd

#model = FastText('train.bin')


def classifier(sentence):
    model = FastText('train.bin')
    return model.predict_proba_single(sentence, k=2)[0][0]

