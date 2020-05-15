import tensorflow as tf
from tensorflow import keras
import pandas as pd
import numpy as np
import io


train_file = "nkjcb_data.csv"
word_vec_file = "wiki-news-300d-1M.vec"
tf.compat.v1.disable_eager_execution()
#tf.compat.v1.enable_eager_execution()
sess = tf.compat.v1.Session()
graph = tf.compat.v1.get_default_graph()
tf.compat.v1.keras.backend.set_session(sess)

model = keras.models.load_model("kj_cb-e13-nd100k.h5")
print(model.summary())

df = pd.read_csv(train_file)
print("df.shape:", df.shape)

n = df.to_numpy()
intents = []
slots = []
for row in n:
    for i, val in enumerate(row):
        if i == 3:
            if val not in intents:
                intents.append(val)
        elif i == 2:
            for slot in val.split():
                if slot not in slots:
                    slots.append(slot)
print(intents)
print(slots)


def vocab(embf=None, n=100000, req=None):
    if not embf:
        embf = word_vec_file

    def load_vectors(fname, n):
        fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
        data = {}
        for i, line in enumerate(fin):
            if i == 0:
                continue
            tokens = line.rstrip().split(' ')
            if i < n:
                data[tokens[0]] = list(map(float, tokens[1:]))
            if req is None and i >= n:
                break
            elif req is not None and tokens[0] in req:
                data[tokens[0]] = list(map(float, tokens[1:]))
        return data

    word_to_vec = {}
    # unk = [0] * 300
    word_to_vec = load_vectors(embf, n)
    return word_to_vec


word_to_vec = vocab(n=1 * 10 ** 5)
print("Loaded word vecs")


def predict(sent):
    global graph, sess
    print("predicting for ", sent)
    tokens = sent.split()
    ip = np.zeros((1, len(tokens), 300))
    for i, token in enumerate(tokens):
        if token in word_to_vec:
            ip[0, i] = word_to_vec[token]
        else:
            ip[0, i] = [0] * 300
    with graph.as_default():
        tf.compat.v1.keras.backend.set_session(sess)
        pred = model.predict(ip)
    intents_pred = pred[0]
    intents_pred = list(np.squeeze(intents_pred))
    # print(intents_pred)
    # print("Intent:", intents[intents_pred.index(max(intents_pred))])
    slots_pred = pred[1]
    slots_pred = np.squeeze(slots_pred)
    ret_slots = ""
    for pred in slots_pred:
        pred = list(pred)
        ret_slots = ret_slots + slots[pred.index(max(pred))] + " "

    # print(ret_slots)
    return {
        "intent": intents[intents_pred.index(max(intents_pred))],
        "intent_probs": intents_pred,
        "slots": ret_slots.strip()
    }


if __name__ == '__main__':
    while True:
        sent = input("Enter\n")
        print(predict(sent))
