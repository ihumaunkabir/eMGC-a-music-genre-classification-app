import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow import keras
import re
import random

# Evaluation of the model
def eval_model(file):
    new_model = tf.keras.models.load_model('model.h5')
    dt = pd.read_csv("features.csv")
    dt.set_index('filename', inplace = True)
    fname = str(re.sub(r'[^a-zA-Z]', '', file[:10])) + ".00000."+ str(random.randint(0,5)) + ".wav"
    testAudio = dt.loc[fname]

    fit = StandardScaler()
    XAudio = fit.fit_transform(np.array(testAudio[:-1], dtype=float).reshape(1,-1))
    prediction = new_model.predict(XAudio)


    return prediction.argmax()


# Finding genre by id
def get_genre(source, id):
    for row in source:
        if id == str( row["id"] ):
            name = row["name"]
            id = str(id)
            desc = row["desc"]

            return id, name, desc
    return "Unknown", "Unknown", "Unknown"


