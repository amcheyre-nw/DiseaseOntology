from owlready2 import *
import ontor
import csv
import pandas as pd
import types


def create_ontology_and_rules():

    onto = get_ontology('disease_ontology.owl')

    # Create Clasess
    with open('disease_classes_2.csv', newline='') as c:
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

    with open('object_props_2.csv', newline='') as op:
        reader1 = csv.reader(op)
        ops = list(reader1)

    new_ops = []
    for line in ops:
        aux = []
        for word in line:
            if " " in word:
                word = word.replace(" ","")
            if "False" in word:
                word = False
            if word == '':
                word = None
            aux.append(word)
        new_ops.append(aux)

    with onto:
        rule = Imp()
        for line in new_classes:
            class1 = line[0]
            superclass1 = line[1]
            if superclass1 == None:
                NewClass = types.new_class(class1, (Thing,))
            else:
                NewClass = types.new_class(superclass1, (Thing,))
                SubClass = types.new_class(class1, (NewClass,))

        for s in new_ops:
            symptom = s[0]
            NewClass = types.new_class(symptom, (ObjectProperty,))

        # Create a list of unique diseases
        unique_diseases = []
        for x in new_classes:
            if x[0] not in unique_diseases:
                unique_diseases.append(x[0])

        # Create a dictionary of all symptoms of a disease
        symptoms_dict = {}
        for disease in unique_diseases:
            symptoms_list = []
            for s in new_ops:
                symptom = s[0]
                if s[3] == disease:
                    symptoms_list.append(symptom)
            symptoms_dict[disease] = symptoms_list

        # Create rules with diseases and symptoms
        rule_set = []
        for i,j in symptoms_dict.items():
            rule_str = ""
            if j != []:
                count = 0
                for s in j:

                    if count < len(j)-1:
                        symptom = s + "(?x, ?y) ^"
                        rule_str = rule_str + symptom
                        count +=1
                    else:
                        symptom = s + "(?x, ?y)"
                        rule_str = rule_str + symptom
                        count += 1
                disease = "->" + i + "(?x)"
                rule_str = rule_str + disease
                print(rule_str)
                rule.set_as_rule("has/Symptoms/Depression(?x, ?y) ^has/Symptoms/Irritability(?x, ?y) ^has/Symptoms/Anxiety(?x, ?y) ->NeuroticDisorders(?x)")
                rule.set_as_rule("has/Symptoms/Depression(?x, ?y)->PhobicDisorders(?x)")
                rule.set_as_rule(rule_str)



    path = os.getcwd()
    onto.save(path+"/disease_ontology_rules.owl")

if __name__ == "__main__":
    create_ontology_and_rules()