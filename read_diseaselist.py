import wikipedia_api as wapi
import pandas as pd
from tqdm import tqdm

disease_names = pd.read_csv('disease_list.csv')['Common name'].to_list()

results = pd.DataFrame(index=['count'])
for d in tqdm(disease_names):
    labels = wapi.retrieveLabels(d)
    if labels is not None:
        for l in labels:
            if l in results.columns:
                results.loc['count', l] += 1
            else:
                results.loc['count', l] = 1
