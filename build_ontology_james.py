import wikipedia_api as wiki
import ULMS_api as ulms
import pandas as pd
from tqdm import tqdm


# first build the disease tree structure and save the instances
api_key = '66bc8361-7450-4750-861c-52ed6ae1dd18'
api = ulms.API(api_key=api_key)

superparent_ui = 'U000014'
#superparent_ui = 'D001523'
#superparent_ui = 'D013001'
#superparent_ui = 'D000068079'

tree, leafs = ulms.build_tree(superparent_ui, api)

treeDF = pd.DataFrame(index=None, columns=['class', 'superclass'])
treeDF['class'] = [t[0] for t in tree[1:]]
treeDF['superclass'] = [t[1] for t in tree[1:]]

# cache
pd.DataFrame(treeDF).to_csv('disease_classes.csv', index=False)

# generate object properties
oprops = pd.DataFrame(index=None, columns=['object_property (op)', 'super-op', 'domain', 'range', 'functional',
                                           'inverse functional', 'transitive', 'symmetric', 'asymmetric',
                                           'reflexive', 'irreflexive', 'inverse_prop']) # initialise container

disease_domain = tree[1][0] # ultimate domain for diseases

# Add UI data property
for row in tree: # this will create duplicates (I think), but we'll delete them later on so no harm done
    _class = row[0]
    _classUI = row[2]
    oprops.loc[len(oprops)] = ['UI/{}'.format(_classUI), None, disease_domain, _class,
                           False, False, False, False, False, False, False, None]

oprops = oprops.drop_duplicates(ignore_index=True)

# generate ALL the labels from wiki (not just symptoms but EVERYTHING)
print('\nBuilding Wiki Properties')
for d in tqdm(leafs[1:]):
    disease_str = d[0]
    labels = wiki.retrieveLabels(disease_str)

    if isinstance(labels, list):

        if '' in labels: # found a weird edge case where '' was a label
            labels.remove('')

        for label in labels:

            if len(label) == 1:
                label = label.upper()
            else:
                label = label[0].upper() + label[1:].lower() # format

            label = label.replace(' ', '_') # remove spaces
            props = wiki.retrieveFacts(disease_str, label)

            if props is not None and len(props) != 0:

                if label == 'wiki_name' and disease_str in props: # if wiki_name is already our main disease name, dont bother
                    props.remove(disease_str)

                elif label == 'Other_names' and disease_str in props:
                    props.remove(disease_str) # don't record our main 'disease_str' as "other name"

                elif label == 'wiki_name' and disease_str not in props: # if wiki_name is something different, add it as an "other name"
                    label = 'Other_names'

                for p in props:
                    oprops.loc[len(oprops)] = ['has/{}/{}'.format(label, p.replace(' ', '_')), None, disease_domain, disease_str,
                                               False, False, False, False, False, False, False, None]

oprops.to_csv('object_props.csv', index=False)
