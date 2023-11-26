import os
import pickle
import progressbar
import numpy as np
import pandas as pd
bar = progressbar.ProgressBar(maxval=18453, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
bar.start()

id = []
data = []
k = 0
for i in os.listdir("./pickles"):
    with open(f"./pickles/{i}", "rb") as f:
        if (k+1) % 10000 == 0:
            pd.DataFrame({"id":id, "data":data}).to_pickle("part1.pd")
            id.clear()
            data.clear()
        try:
            _data = pickle.load(f)
            bar.update(k:=k+1)
            id.append(i[:-7])
            data.append(_data)
        except:
            print(i)
pd.DataFrame({"id":id, "data":data}).to_pickle("part2.pd")
id.clear()
data.clear()
bar.finish()