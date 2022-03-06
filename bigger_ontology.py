from owlready2 import *
import ontor
import re
import csv
import pandas as pd
import types
from random import randrange
from pydoc import locate

def create_ontology_and_rules():
    path = os.getcwd()
    onto = get_ontology('disease_ontology_trial.owl')

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

    with open('object_props_SMED_inherited2.csv', newline='') as op:
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
    # Create rules for all the classes
        rule_count = 0
        sym_count = 0
        spec_count = 0
        risk_count = 0
        freq_count = 0
        caus_count = 0
        prog_count = 0
        med_count = 0
        comp_count = 0
        other_count = 0
        max_per_class = 6
        for i,j in dict.items():
            pred = i
            # Symptoms
            if i == 'Symptoms':
                for x,y in j.items():
                    if sym_count < max_per_class and x in (item[0] for item in new_classes):
                        dis = x
                        rule_sym = ""
                        abc = "abcdefghijklmnopqrstuvwxyz"
                        x = 0
                        for n in range(len(y)):
                            s = y[n]
                            a = abc[x]
                            symptom = "has"+pred+"(?x,?"+a+") ^" + s + "(?"+a+") ^"
                            rule_sym = rule_sym + symptom
                            x += 1

                        i = i.replace(",", "")
                        disease = "->" + dis + "(?x)"
                        rule_sym = rule_sym + disease
                        print(rule_sym)
                        rule = Imp()
                        rule.set_as_rule(rule_sym)
                        print(i)
                        print(sym_count)
                        sym_count += 1


            # Speciality
            if i == 'Speciality':
                for x, y in j.items():
                    if spec_count < max_per_class and x in (item[0] for item in new_classes):
                        dis = x
                        rule_comp = ""
                        rand = randrange(len(y))
                        complication = y[rand] + "(?x)"
                        rule_comp = rule_comp + complication

                        disease = dis + "(?x) ->"
                        rule_comp = disease + rule_comp
                        print(rule_comp)
                        rule = Imp()
                        rule.set_as_rule(rule_comp)
                        print(i)
                        print(spec_count)
                        spec_count += 1

            # Medication
            if i == 'Medication':
                for x, y in j.items():
                    if med_count < max_per_class and x in (item[0] for item in new_classes):
                        dis = x
                        rule_med = ""
                        rand = randrange(len(y))
                        medication = y[rand] + "(?x)"
                        rule_med = rule_med + medication

                        disease = dis + "(?x) ->"
                        rule_med = disease + rule_med
                        print(rule_med)
                        rule = Imp()
                        rule.set_as_rule(rule_med)
                        print(i)
                        print(med_count)
                        med_count += 1

            # Frequency
            if i == 'Frequency':
                for x, y in j.items():
                    if freq_count < max_per_class and x in (item[0] for item in new_classes):
                        dis = x
                        rule_comp = ""
                        rand = randrange(len(y))
                        if y[rand].isalpha()== True:
                            complication = y[rand].replace('_',"") + "(?x)"
                            rule_comp = rule_comp + complication

                            disease = dis + "(?x) ->"
                            rule_comp = disease + rule_comp
                            print(rule_comp)
                            rule = Imp()
                            #rule.set_as_rule(rule_comp)
                            print(i)
                            print(freq_count)
                            freq_count += 1

            # Other_names
            if i == 'Other_names':
                for x, y in j.items():
                    if other_count < max_per_class and x in (item[0] for item in new_classes):
                        dis = x
                        rule_comp = ""
                        rand = randrange(len(y))
                        other_name = y[rand] + "(?x)"
                        rule_comp = rule_comp + other_name

                        disease = dis + "(?x) ->"
                        rule_comp = disease + rule_comp
                        print(rule_comp)
                        rule = Imp()
                        rule.set_as_rule(rule_comp)
                        print(i)
                        print(other_count)
                        other_count += 1

            # Causes
            if i == 'Causes':
                for x, y in j.items():
                    if caus_count < max_per_class and x in (item[0] for item in new_classes):
                        dis = x
                        rule_comp = ""

                        rand = randrange(len(y))
                        cause = y[rand] + "(?x)"
                        rule_comp = rule_comp + cause

                        disease = dis + "(?x) ->"
                        rule_comp = disease + rule_comp
                        print(rule_comp)
                        rule = Imp()
                        rule.set_as_rule(rule_comp)
                        print(i)
                        print(caus_count)
                        caus_count += 1

            # Complications
            if i == 'Complications':
                for x, y in j.items():
                    if comp_count < max_per_class and x in (item[0] for item in new_classes):
                        dis = x
                        rule_comp = ""
                        rand = randrange(len(y))
                        complication = y[rand] + "(?x)"
                        rule_comp = rule_comp + complication

                        disease = dis + "(?x) ->"
                        rule_comp = disease + rule_comp
                        print(rule_comp)
                        rule = Imp()
                        rule.set_as_rule(rule_comp)
                        print(i)
                        print(comp_count)
                        comp_count += 1
                        print(rule_comp)

            # Prognosis
            if i == 'Prognosis':
                for x, y in j.items():
                    if prog_count < max_per_class and x in (item[0] for item in new_classes):
                        dis = x
                        rule_comp = ""
                        rand = randrange(len(y))
                        complication = y[rand] + "(?x)"
                        rule_comp = rule_comp + complication

                        disease = dis + "(?x) ->"
                        rule_comp = disease + rule_comp
                        print(rule_comp)
                        rule = Imp()
                        rule.set_as_rule(rule_comp)
                        print(i)
                        print(prog_count)
                        prog_count += 1

            # Risk_factors
            if i == 'Risk_factors':
                for x, y in j.items():
                    if risk_count < max_per_class and x in (item[0] for item in new_classes):
                        dis = x
                        rule_comp = ""
                        rand = randrange(len(y))
                        complication = y[rand] + "(?x)"
                        rule_comp = rule_comp + complication

                        disease = dis + "(?x) ->"
                        rule_comp = disease + rule_comp
                        print(rule_comp)
                        rule = Imp()
                        rule.set_as_rule(rule_comp)
                        print(i)
                        print(risk_count)
                        risk_count += 1


    onto.save(path+"/disease_ontology_trial.owl")

if __name__ == "__main__":
    create_ontology_and_rules()

