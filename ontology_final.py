from owlready2 import *
import ontor
import csv
import pandas as pd
import types


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

    with open('object_props_SMED_inherited_2.csv', newline='') as op:
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

        for line in new_classes:
            class1 = line[0]
            superclass1 = line[1]
            if superclass1 == None:
                NewClass = types.new_class(class1, (Thing,))
            else:
                NewClass = types.new_class(str(superclass1).replace(",",""), (Thing,))
                SubClass = types.new_class(str(class1).replace(",",""), (NewClass,))

        for s in new_ops:
            symptom = s[0]
            if type(symptom) == str:
                NewClass = types.new_class(symptom.replace(",",""), (ObjectProperty,))

        # Create a list of unique diseases
        unique_diseases = []
        for x in new_classes:
            if x[0] not in unique_diseases:
                unique_diseases.append(x[0])

        # Create a dictionary of all symptoms, medications and complications of a disease
        symptoms_dict = {}
        for disease in unique_diseases:
            symptoms_list = []
            disease = disease.replace(",","")
            for s in new_ops:
                symptom = s[0]

                if s[3].replace(",","") == disease:
                    symptoms_list.append(symptom)
            symptoms_dict[disease] = symptoms_list


        # Count symptoms per disease
        symp_count = {}
        for i,j in symptoms_dict.items():
            sym = 0
            if j != []:
                for s in j:
                    s = str(s)
                    s = s.replace(",", "")
                    if "hasSymptoms" in s:
                        sym += 1
            symp_count[i] = sym

        # Create rules with diseases and symptoms
        rule_count = 0
        sym_count = 0
        med_count = 0
        comp_count = 0
        for i,j in symptoms_dict.items():
            if rule_count < 60:
                rule_sym = ""
                rule_comp = ""
                rule_med = ""
                if j != []:
                    count = 0
                    for s in j:
                        s = str(s)
                        s = s.replace(",","")
                        if "hasSymptoms" in s:
                            symptom = s + "(?x, ?y) ^"
                            rule_sym = rule_sym + symptom
                            count +=1

                        if "hasComplications" in s:
                            complication = s + "(?x, ?y) ^"
                            rule_comp = rule_comp + complication
                            count +=1

                        if "hasMedication" in s:
                            medication = s + "(?x, ?y) ^"
                            rule_med = rule_med + medication
                            count +=1

                    i = i.replace(",","")

                    rule = Imp()
                    if rule_sym != "":
                        disease = "->" + i + "(?x)"
                        rule_sym = rule_sym + disease
                        rule.set_as_rule(rule_sym)
                        rule_count += 1
                    if rule_comp != "":
                        disease = "->" + i + "(?x)"
                        rule_comp = rule_comp + disease
                        rule.set_as_rule(rule_comp)
                        rule_count += 1
                    if rule_med != "":
                        disease = "->" + i + "(?x)"
                        rule_med = rule_med + disease
                        rule.set_as_rule(rule_med)
                        rule_count += 1

                    print(rule_sym)
                    print(rule_comp)
                    print(rule_med)
                    print(rule_count)

    onto.save(path+"/disease_ontology_SMED.owl")

if __name__ == "__main__":
    create_ontology_and_rules()