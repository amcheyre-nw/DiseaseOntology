import wikipedia_api as wiki
import ULMS_api as ulms
import pandas as pd
from tqdm import tqdm
import numpy as np


def build_hierarchy(superparent_ui):
    # first build the disease tree structure and save the instances
    api_key = '66bc8361-7450-4750-861c-52ed6ae1dd18'
    api = ulms.API(api_key=api_key)

    tree = ulms.build_tree_inverse_isa(superparent_ui, api, sourcename='SNOMEDCT_US')

    treeDF = pd.DataFrame(index=None, columns=['class', 'superclass'])
    treeDF['class'] = [t[0] for t in tree[1:]]
    treeDF['superclass'] = [t[1] for t in tree[1:]]

    # cache
    pd.DataFrame(treeDF).to_csv('disease_classes_SMED.csv', index=False)
    return


def gen_object_properties(treeDF, labels=None):

    # generate object properties
    oprops = pd.DataFrame(index=None, columns=['object_property (op)', 'super-op', 'domain', 'range', 'functional',
                                               'inverse functional', 'transitive', 'symmetric', 'asymmetric',
                                               'reflexive', 'irreflexive', 'inverse_prop']) # initialise container

    disease_domain = treeDF.iloc[1,0] # ultimate domain for diseases

    # Add UI data property
#    for row in treeDF: # this will create duplicates (I think), but we'll delete them later on so no harm done
#        _class = row.iloc[0]
#        _classUI = row.iloc[2]
#        oprops.loc[len(oprops)] = ['UI/{}'.format(_classUI), None, disease_domain, _class,
#                               False, False, False, False, False, False, False, None]

    oprops = oprops.drop_duplicates(ignore_index=True)

    # generate ALL the labels from wiki (not just symptoms but EVERYTHING)
    print('\nBuilding Wiki Properties')
    for d in treeDF.iloc[:,0].unique():
        disease_str = d

        if labels is None:
            labels = wiki.retrieveLabels(disease_str)

        #labels = ['Symptoms'] # just stick to these right now
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

                print('disease {} | label {} | values {}'.format(disease_str, label, props))

    oprops.to_csv('object_props_SMED.csv', index=False)
    return


def get_parents(tree, childname):
    result = tree.loc[tree['class']==childname]['superclass'].to_list()

    if np.nan in result:
        result.remove(np.nan)
    if len(result) > 0:
        return result
    else:
        return None


def gen_inherited_properties(tree, properties, N):
    '''

    :param tree: dataframe of class/superclass structure
    :param properties: pythonic dataframe of data properties within the tree
    :param N: number of paths a property can be inherited over
    :return:
    '''

    uniques = tree.iloc[:,0].unique()
    new_props =  pd.DataFrame(index=None, columns=['object_property (op)', 'super-op', 'domain', 'range', 'functional',
                                               'inverse functional', 'transitive', 'symmetric', 'asymmetric',
                                               'reflexive', 'irreflexive', 'inverse_prop']) # initialise container

    domain = properties.iloc[0]['domain'] # hack

    for node in tqdm(uniques):

        # get Nth ancestors of node
        ancestors = []
        stack = [[node, 0]] # use syntax [node, distance]
        while len(stack) > 0:
            root, distance = stack.pop(0)
            parents = get_parents(tree, root)

            if parents is not None:
                ancestors = ancestors + parents

                if distance < N:
                    stack = stack + [[p, distance+1] for p in parents]

        node_props = properties.loc[properties['range'] == node, 'object_property (op)'] # already existing props

        # NB: We only inherit properties if they don't exist already
        node_prop_types = [n.split('/')[1] for n in node_props]

        for anc in ancestors:
            anc_props = properties.loc[properties['range']==anc]['object_property (op)']
            for ap in anc_props:
                prop_type = ap.split('/')[1]
                if prop_type not in node_prop_types: # only add in if doesn't exist
                    node_props = pd.concat([node_props, anc_props])

        for prop in node_props.unique(): # now regenerate the properties
            new_props.loc[len(new_props)] = [prop, None, domain, node,
                                       False, False, False, False, False, False, False, None]

    new_props.to_csv('object_props_SMED_inherited.csv', index=False)
    return


if __name__ == "__main__":
    #build_hierarchy('74732009')
    treeDF = pd.read_csv('disease_classes_SMED.csv')
    #gen_object_properties(treeDF, labels=['Symptoms', 'Complications', 'Speciality', 'Medication', 'Frequency', 'Other names'])
    obj_props = pd.read_csv('object_props_SMED2.csv')
    gen_inherited_properties(treeDF, obj_props, 2)


