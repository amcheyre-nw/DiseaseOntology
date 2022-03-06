import wikipedia_api
import wikipedia_api as wiki
import ULMS_api as ulms
import pandas as pd
from tqdm import tqdm
import numpy as np
from duckduckgo_api import get_wikititle_from_queery


def build_hierarchy(superparent_ui, sourcename="SNOMEDCT_US"):
    # first build the disease tree structure and save the instances
    api_key = '66bc8361-7450-4750-861c-52ed6ae1dd18'
    api = ulms.API(api_key=api_key)

    tree = ulms.build_tree_inverse_isa(superparent_ui, api, sourcename=sourcename)

    treeDF = pd.DataFrame(index=None, columns=['class', 'superclass'])
    treeDF['class'] = [t[0] for t in tree[1:]]
    treeDF['superclass'] = [t[1] for t in tree[1:]]

    # cache
    pd.DataFrame(treeDF).to_csv('disease_classes_SMED.csv', index=False)
    return


def gen_object_properties(treeDF, labelDict=None, priorpass=None, filename='object_properties_SMED.csv',
                          duckduckgo_backup=False):
    '''

    :param treeDF:  DataFrame containing first column, classes we want to investigate
    :param label_names: dictionary mapping the label we're after along with kwargs in getting the label
    :param prior pass: list of all the values that have been scraped in a prior run, for string matching
    :param duckduckgo_backup: bool. If true, use duckduckgo api to find the correct name of wiki articles when the
    normal process doesn't work.
    :return:
    '''
    # generate object properties
    oprops = pd.DataFrame(index=None, columns=['object_property (op)', 'super-op', 'domain', 'range', 'functional',
                                               'inverse functional', 'transitive', 'symmetric', 'asymmetric',
                                               'reflexive', 'irreflexive', 'inverse_prop'])  # initialise container

    disease_domain = treeDF.iloc[1, 0]  # ultimate domain for diseases

    # Add UI data property
    #    for row in treeDF: # this will create duplicates (I think), but we'll delete them later on so no harm done
    #        _class = row.iloc[0]
    #        _classUI = row.iloc[2]
    #        oprops.loc[len(oprops)] = ['UI/{}'.format(_classUI), None, disease_domain, _class,
    #                               False, False, False, False, False, False, False, None]

    oprops = oprops.drop_duplicates(ignore_index=True)

    # generate ALL the labels from wiki (not just symptoms but EVERYTHING)
    print('\nBuilding Wiki Properties')
    for d in treeDF.iloc[:, 0].unique():
        disease_str = d

        for label in labelDict.keys():

            if len(label) == 1:
                label = label.upper()
            else:
                label = label[0].upper() + label[1:].lower()  # format

            delimeter = labelDict[label]['delimiter']
            # here we make an exception if label=speciality. Turns out specialty is also used, so we look for both and concat
            if label=='Speciality':
                props1 = wiki.retrieveFacts(disease_str, "Speciality", delimeter=delimeter, duckduckgo_backup=duckduckgo_backup)
                props2 = wiki.retrieveFacts(disease_str, "Specialty", delimeter=delimeter, duckduckgo_backup=duckduckgo_backup)
                if props1 is None:
                    props1 = []
                if props2 is None:
                    props2 = []
                props = props1 + props2
            else:
                props = wiki.retrieveFacts(disease_str, label, delimeter=delimeter, duckduckgo_backup=duckduckgo_backup)

            label = label.replace(' ', '_')  # remove spaces

            if label == 'Other_names' and duckduckgo_backup:
                ddg_name = get_wikititle_from_queery(disease_str)
                if props is None:
                    props=[]
                try:
                    props.remove(ddg_name)  # try and remove it first to stop duplication
                except:
                    pass
                if isinstance(ddg_name, str):
                    props.append(ddg_name)

            if props is not None and len(props) != 0:

                if priorpass is not None:
                    assert isinstance(priorpass, pd.DataFrame)
                    assert delimeter == None
                    pp_label = priorpass.loc[
                        priorpass['object_property (op)'].str.split('/').str[1].str.lower() == label.lower()]
                    pp_values = pp_label['object_property (op)'].str.split('/').str[-1].str.replace('_', ' ').str.lower().unique()

                    if len(props) > 1:
                        text = ' '.join(props)
                    else:
                        text = props[0]

                    props = [p for p in pp_values if p in text] # keep any words we've seen in the priorpass

                if label == 'Other_names' and disease_str in props:
                    props.remove(disease_str)  # don't record our main 'disease_str' as "other name"


                for p in props:
                    oprops.loc[len(oprops)] = ['has/{}/{}'.format(label, p.replace(' ', '_')), None, disease_domain,
                                               disease_str,
                                               False, False, False, False, False, False, False, None]

            print('disease {} | label {} | values {}'.format(disease_str, label, props))

    if priorpass is not None: # we want to stick them together and then remove duplicates
        oprops = pd.concat([priorpass, oprops], axis=0).drop_duplicates(ignore_index=True)

    oprops.to_csv(filename, index=False)
    return oprops


def get_parents(tree, childname):
    result = tree.loc[tree['class'] == childname]['superclass'].to_list()

    if np.nan in result:
        result.remove(np.nan)
    if len(result) > 0:
        return result
    else:
        return None


def wiki_corpus_prune(disease, object_props, thresh=1):
    '''

    For a disease, pull the sumamry text from wikipedia and only keep symptoms that appear in the summary text.
    :param disease: disease to look up on wikipedia
    :param object_props: df of the object properties
    :param thresh: number of occurences needed in the corpus to justify keeping
    :return:
    '''

    summary = wikipedia_api.get_wiki_summary(disease)
    object_props = object_props.to_list()

    for prop in object_props:
        count = summary.count(prop.lower())
        if count < thresh:
            object_props.remove(prop)
    return object_props


def gen_inherited_properties(tree, properties, N):
    '''

    :param tree: dataframe of class/superclass structure
    :param properties: pythonic dataframe of data properties within the tree. ie: object_class dataframe from gen_object_properties()
    :param N: number of paths a property can be inherited over
    :return:
    '''

    uniques = tree.iloc[:, 0].unique()
    new_props = pd.DataFrame(index=None, columns=['object_property (op)', 'super-op', 'domain', 'range', 'functional',
                                                  'inverse functional', 'transitive', 'symmetric', 'asymmetric',
                                                  'reflexive', 'irreflexive', 'inverse_prop'])  # initialise container

    domain = properties.iloc[0]['domain']  # hack

    for node in tqdm(uniques):

        # get Nth ancestors of node
        ancestors = []
        stack = [[node, 0]]  # use syntax [node, distance]
        while len(stack) > 0:
            root, distance = stack.pop(0)
            parents = get_parents(tree, root)

            if parents is not None:
                ancestors = ancestors + parents

                if distance < N:
                    stack = stack + [[p, distance + 1] for p in parents]

        node_props = properties.loc[properties['range'] == node, 'object_property (op)']  # already existing props

        # NB: We only inherit properties if they don't exist already
        node_prop_types = [n.split('/')[1] for n in node_props]

        for anc in ancestors:
            anc_props = properties.loc[properties['range'] == anc]['object_property (op)']
            anc_props = pd.Series(wiki_corpus_prune(node, anc_props, thresh=1))
            for ap in anc_props:
                prop_type = ap.split('/')[1]
                if prop_type not in node_prop_types:  # only add in if doesn't exist
                    node_props = pd.concat([node_props, anc_props])

        for prop in node_props.unique():  # now regenerate the properties
            new_props.loc[len(new_props)] = [prop, None, domain, node,
                                             False, False, False, False, False, False, False, None]

    new_props.to_csv('object_props_SMED_inherited.csv', index=False)
    return


if __name__ == "__main__":
    #build_hierarchy('74732009', sourcename="SNOMEDCT_US")
    #build_hierarchy("C0033975", sourcename="CUI")
    treeDF = pd.read_csv('disease_classes_SMED.csv')
    #treeDF.iloc[0, 0] = 'Organic mental disorder'
    #treeDF.iloc[0, 0] = 'Factitious disorder imposed on another'

#    ops = gen_object_properties(treeDF,
#                          labelDict={
#                                     'Symptoms':        {"delimiter": "hyperlinks"},
#                                     'Complications':   {"delimiter": "hyperlinks"},
#                                     'Speciality':      {"delimiter": "hyperlinks"},
#                                     'Medication':      {"delimiter": "hyperlinks"},
#                                     'Frequency':       {"delimiter": None},
#                                     'Other names':     {"delimiter": ","}, # Other names are always either comma or
#                                     'Prognosis':       {"delimiter": None},
#                                     'Causes':          {"delimiter": ","},
#                                     'Risk factors':    {"delimiter": ","}
#                                     },
#                          duckduckgo_backup=True,
#                          filename='object_properties_SMED.csv'
#                                )
#
#    ops = pd.read_csv('object_properties_SMED.csv')
#
#    ops2 = gen_object_properties(treeDF,
#                          labelDict={
#                                     'Symptoms':        {"delimiter": None},
#                                     'Complications':   {"delimiter": None},
#                                     'Speciality':      {"delimiter": None},
#                                     'Medication':      {"delimiter": None},
#                                     'Frequency':       {"delimiter": None},
#                                     'Other names':     {"delimiter": None}, # Other names are always either comma or
#                                     'Prognosis':       {"delimiter": None},
#                                     'Causes':          {"delimiter": None},
#                                     'Risk factors':    {"delimiter": None}
#                                     },
#                                 priorpass=ops,
#                                 filename='object_properties_SMED_2pass.csv',
#                                 duckduckgo_backup=True
#                          )

    ops2 = pd.read_csv('object_properties_SMED_2pass.csv')
    ops3 = gen_inherited_properties(treeDF, ops2, 3)



    # obj_props = pd.read_csv('object_props_SMED2.csv')
    # gen_inherited_properties(treeDF, obj_props, 3)
