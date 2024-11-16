import numpy as np
import cryptpandas as cpd

df = cpd.read_encrypted(path='./data/release_5147.crypt', password='MwCvLvuQlJsZMr1I')
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(how="all", inplace=True)
arr = np.array(df.cumsum().tail(1))[0]
print(arr)

def greedy_allocate(arr):
    ranked = list(sorted(arr, key=abs,reverse=True))[:10]
    weights = [0] * len(arr)
    for i, n in enumerate(arr):
        if n in ranked:
            weights[i] = 0.1 if n > 0 else -0.1
    return weights

def convert_to_submission(weights):
    res = dict()
    for i in range(len(weights)):
        res[f"strat_{i}"] = weights[i]
    res['team_name'] = 'Yoghurt'
    res['passcode'] = 'yoghurt'
    return res


print(convert_to_submission(greedy_allocate(arr)))