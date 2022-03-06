from owlready2 import *
import ontor
import re
import csv
import pandas as pd
import types
from pydoc import locate

def create_ontology_and_rules():
    path = os.getcwd()
    onto = get_ontology('disease_ontology_SMED.owl')

    # Create Clasess
    with open('disease_classes_SMED.csv', newline='') as c:
        reader2 = csv.reader(c)
        classes = list(reader2)

    new_classes = []
    for line in classes:
        aux = []
        for word in line:
            if " " in word:
                word = word.replace(" ","")
            if word == '':
                word = None
            aux.append(word)
        new_classes.append(aux)

    with open('/Users/anerypatel/Desktop/object_props_SMED_2.csv', newline='') as op:
        reader1 = csv.reader(op)
        ops = list(reader1)

    new_ops = []
    for line in ops:
        aux = []
        for word in line:
            word = word.strip(')')
            word = word.strip(' ')
            word = word.strip('.')
            if " " in word:
                word = word.replace(" ","")
            if "False" in word:
                word = False
            if word == '':
                word = None
            aux.append(word)
        new_ops.append(aux)


    dict = {}
    new_ops = new_ops[1:]

    for line in new_ops:

        disease = line[3]
        property = line[0]
        if type(property) == type(True) or property == None:
            continue

        # split the property 'has/Symptom/Anxiety' into 'Symptom' as predicate and 'Anxiety' as label
        values = property.split('/')
        predicate = values[1]
        label = values[2]
        label = re.sub('[^0-9a-zA-Z]+', '_', label)

        # Create a dictionary >> {Symptom: {} , Complication:{}, Medication:{}, ... }
        # Each nested dictionary will have >> Symptom : {Disease1 : [<list of symptoms>], Disease2 : [<list of symptoms>], .. }
        if predicate not in dict:
            dict[predicate] = {disease:[label]}
        else:
            if disease not in dict[predicate]:
                dict[predicate][disease] = [label]
            else:
                dict[predicate][disease].append(label)


    with onto:
        DiseaseClass = types.new_class('Disease', (Thing,))

        new_classes = list(set(tuple(row) for row in new_classes))

        predicateClass = {}
        for predicate in dict.keys():
            PredicateClass = types.new_class(predicate, (Thing,))
            predicateClass[predicate] = PredicateClass
            property = 'has'+predicate
            PropertyClass = types.new_class(property, (ObjectProperty,))


        for line in new_classes:
            class1 = line[0]
            superclass1 = line[1]
            if superclass1 == None:
                Disease = types.new_class(class1, (DiseaseClass,))
            else:
                SuperClass = types.new_class(str(superclass1).replace(",",""), (DiseaseClass,))
                Disease = types.new_class(str(class1).replace(",",""), (SuperClass,))

            for predicate in dict.keys():
                if class1 in dict[predicate].keys():
                    allLabels = []
                    for label in dict[predicate][class1]:
                        Label = types.new_class(label, (predicateClass[predicate],))
                        allLabels.append(Label)
                    setattr(Disease, 'has'+predicate, allLabels)

# rules start from here


    onto.save(path+"/disease_ontology_trial.owl")

if __name__ == "__main__":
    create_ontology_and_rules()

