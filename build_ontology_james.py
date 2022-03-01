import wikipedia_api as wiki
import ULMS_api as ulms
import pandas as pd
from tqdm import tqdm


# first build the disease tree structure and save the instances
api_key = '66bc8361-7450-4750-861c-52ed6ae1dd18'
api = ulms.API(api_key=api_key)

#superparent_ui = 'U000014'
superparent_ui = 'D001523'
tree, leafs = ulms.build_tree(superparent_ui, api)

treeDF = pd.DataFrame(index=None, columns=['class', 'superclass'])
treeDF['class'] = [t[0] for t in tree[1:]]
treeDF['superclass'] = [t[1] for t in tree[1:]]

# cache
pd.DataFrame(tree).to_csv('disease_classes.csv')

# use wikipedia to generate symptom properties
oprops = pd.DataFrame(index=None, columns=['object_property (op)', 'super-op', 'domain', 'range', 'functional',
                                           'inverse functional', 'transitive', 'symmetric', 'asymmetric',
                                           'reflexive', 'irreflexive', 'inverse_prop'])

disease_domain = tree[1][0] # ultimate domain for diseases

print('\nBuilding object properties')
for d in tqdm(leafs):
    disease_str = d[0]
    props = wiki.retrieveFacts(disease_str, "Symptoms")
    if props is not None:
        for p in props:
            oprops.loc[len[oprops]] = ['hasSymptom{}'.format(p), None, disease_domain, d,
                                       False, False, False, False, False, False, False, None]

oprops.to_csv('object_props.csv')
