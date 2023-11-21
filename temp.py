import os
import librosa
from Embeddings.Embed import Embedder
import struct
import numpy as np
import pandas as pd
import pickle

emb = Embedder(max_duration_seconds=167.24)
vector_dimension = 144000
data = pd.DataFrame({"Id":[], "Vector":[]})
PATH = "../https-github.com-yoyonel-audio-fingerprint-identifying-python/mp3/"
with open("tracks.id", "wb") as f_id:
    for i in os.listdir(PATH):
        if i.endswith(".mp3") and not os.path.exists("pickles/"+i+".pk"):
            with open("pickles/"+i+".pk", "wb") as f_features:
                features =  emb.get_mfcc_features_flatenized(PATH+i)
                if features.shape[0] > vector_dimension:
                    features = features[:vector_dimension]

                if features.shape[0] < vector_dimension:
                    # Repeat the last row until the dimension is the same
                    features = np.pad(features, (0, vector_dimension - features.shape[0]),
                                    'edge')
                pickle.dump(features, f_features)
        else:
            print("SKIPPING", "pickles/"+i+".pk")