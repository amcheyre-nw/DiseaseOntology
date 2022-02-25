import wikipedia_api as wapi
import pandas as pd
from tqdm import tqdm
from owlready2 import *
import ontor


def create_ontology(classes=None, ops=None, dps=None, axs=None, ins=None):

    # https://{hostdomain}/{ontologiesRoot}/{authority}/{resourceIdentifier}.owl
    iri = "http://example.org/disease_ontology.owl"
    fname = "./disease_ontology.owl"
    path = os.getcwd()
    ontor1 = ontor.OntoEditor(iri, fname)

    # Add the information as lists
    if classes is not None:
        ontor1.add_taxo(classes)
    if ops is not None:
        ontor1.add_ops(ops)
    #ontor1.add_dps(dps)
    #ontor1.add_axioms(axs)
    if ins is not None:
        ontor1.add_instances(ins)

    ontor1.save_as(path + "/disease_ontology.owl")

    # Visualize a graph
    # ontor1.visualize(classes=["human", "pizza"], properties=["likes", "diameter_in_cm"], focusnode="John", radius=2)
    return


def retrieve_subtree(list, subfields=['Symptom', 'Causes', 'Treatment', 'Prevention', 'Complications']):
    results = pd.DataFrame(columns=['Subject', 'Subfield', 'Value'])
    for d in tqdm(list):
        labels = wapi.retrieveLabels(d)
        if labels is not None:
            labels = [l for l in labels if l in subfields]
            for l in labels:
                info = wapi.retrieveFacts(d, l)
                if info is not None:
                    for i in info:
                        N = len(results)
                        results.loc[N, ['Subject', 'Subfield']] = [d, l]
                        results.loc[N, 'Value'] = i
    return results


def build_tree(list, subj_name, depth=0, max_depth=1):
    data = retrieve_subtree(list)

    classes = [[subj_name, None]]

    labels = data['Subfield'].unique()
    relations = [[row[1]['Subject'],
                  row[1]['Value'],
                  "is{}Of".format(row[1]['Subfield']), None, None] for row in data.iterrows()]

    if depth < 1:
        for l in labels:
            mask = (data['Subfield']==l)
            subdata = data[mask]['Value'].unique()
            next_level = build_tree(subdata, l, depth=depth+1)
            if next_level is not None:
                classes, relations = classes + next_level[0], relations + next_level[1]

    return classes, relations


disease_names = pd.read_csv('disease_list.csv')['Common name'].to_list()
classes, relations = build_tree(disease_names, "Disease", max_depth=2)

# Properties of objects including their axioms
# [object_property (op), super-op, domain, range,functional, inverse functional, transitive, symmetric,
# asymmetric, reflexive, irreflexive, inverse_prop]
ops = [["isSymptomOf", None, "Disease", None, False, False, False, False, False, False, False, None],
       ["isComplicationOf", None, "Disease",None, False, False, False, False, False, False, False, None],
       ["isCauseOf", None, "Disease", None, False, False, False, False, False, False, False, None],
       ["isTreatmentOf", None, "Disease", None, False, False, False, False, False, False, False, None],
       ["isPreventionOf", None, "Disease", None, False, False, False, False, False, False, False, None]]

# Axioms: [class, superclass, property, inverted(bool), cardinality type, cardinality, op-object, dp-range,
#         dp-min-ex, dp-min-in, dp-exact, dp-max-in, dp-max-ex, negated(bool), equivalence(bool)]
#axs = [["human", None, "likes", None, "some", None, "food", None, None, None, None, None, None, None, False]]

# remove duplicates
classes_unique = []
relations_unique = []
for x in classes:
    if x not in classes_unique:
        classes_unique.append(x)
for x in relations:
    if x not in relations_unique:
        relations_unique.append(x)


create_ontology(classes=classes_unique,
                ins=relations_unique,
                ops=ops)

print('done')
