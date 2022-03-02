import pandas as pd

csv = pd.read_csv('disease_classes_SMED.csv')

for idx in range(1, len(csv)):
    above = csv.iloc[0:idx,0].to_list()
    if csv.iloc[idx, 1] not in above:
        data = csv.iloc[idx].copy()
        index = csv.index[idx]
        csv = csv.drop(index=index)
        csv = pd.concat([csv, pd.DataFrame(data).transpose()[['class', 'superclass']]])

csv.to_csv('new.csv', index=False)
