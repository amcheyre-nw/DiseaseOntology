from owlready2 import *
import ontor
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

    #unique_diseases = list(set(new_classes))

    symptoms_dict = {}
    medications_dict = {}
    complications_dict = {}

    for line in new_ops:
        disease = line[3]
        property = line[0]
        if type(property) == type(True):
            continue

        if 'Symptom' in property:
            property = property.replace('hasSymptoms', '')
            if disease not in symptoms_dict:
                symptoms_dict[disease] = [property]
            else:
                symptoms_dict[disease].append(property)
        if 'Medication' in property:
            property = property.replace('hasMedication', '')
            if disease not in medications_dict:
                medications_dict[disease] = [property]
            else:
                medications_dict[disease].append(property)
        if 'Complication' in property:
            property = property.replace('hasComplications', '')
            if disease not in complications_dict:
                complications_dict[disease] = [property]
            else:
                complications_dict[disease].append(property)

    with onto:
        DiseaseClass = types.new_class('Disease', (Thing,))
        SymptomClass = types.new_class('Symptom', (Thing,))
        MedicationClass = types.new_class('Medication', (Thing,))
        ComplicationClass = types.new_class('Complication', (Thing,))

        hasSymptomclass = types.new_class('hasSymptom', (ObjectProperty,))
        hasSymptomclass.domain = []
        hasSymptomclass.range = []
        hasMedicationclass = types.new_class('hasMedication', (ObjectProperty,))
        hasMedicationclass.domain = []
        hasMedicationclass.range = []
        hasComplicationclass = types.new_class('hasComplication', (ObjectProperty,))
        hasComplicationclass.domain = []
        hasComplicationclass.range = []

        for line in new_classes:
            class1 = line[0]
            superclass1 = line[1]
            if superclass1 == None:
                Disease = types.new_class(class1, (DiseaseClass,))
            else:
                SuperClass = types.new_class(str(superclass1).replace(",",""), (DiseaseClass,))
                Disease = types.new_class(str(class1).replace(",",""), (SuperClass,))

            if class1 in symptoms_dict:
                for symptoms in symptoms_dict[class1]:
                    Symptom = types.new_class(symptoms, (SymptomClass,))
                    hasSymptomclass.domain.append(Disease)
                    hasSymptomclass.range.append(Symptom)

            if class1 in medications_dict:
                for medications in medications_dict[class1]:
                    Medication = types.new_class(medications, (MedicationClass,))
                    hasMedicationclass.domain.append(Disease)
                    hasMedicationclass.range.append(Medication)

            if class1 in complications_dict:
                for complications in complications_dict[class1]:
                    Complication = types.new_class(complications, (ComplicationClass,))
                    hasComplicationclass.domain.append(Disease)
                    hasComplicationclass.range.append(Complication)


        # Create rules with diseases and symptoms
        rule_count = 0
        sym_count = 0
        med_count = 0
        comp_count = 0
        for i,j in symptoms_dict.items():
            if sym_count < 15:
                rule_sym = ""
                if j != []:
                    for s in j:
                        s = str(s)
                        s = s.replace(",","")
                        symptom = s + "(?x, ?y) ^"
                        rule_sym = rule_sym + symptom

                i = i.replace(",", "")
                disease = "->" + i + "(?x)"
                rule_sym = rule_sym + disease
                rule = Imp()
                rule.set_as_rule(rule_sym)
                sym_count += 1
                print(rule_sym)

        for i, j in complications_dict.items():
            if comp_count < 15:
                rule_comp = ""
                if j != []:
                    complication = j[0] + "(?x, ?y) ^"
                    rule_comp = rule_comp + complication

                i = i.replace(",", "")
                disease = i + "(?x) ->"
                rule_comp = disease + rule_comp
                rule = Imp()
                rule.set_as_rule(rule_comp)
                comp_count += 1
                print(rule_comp)

        for i, j in medications_dict.items():
            if comp_count < 15:
                rule_comp = ""
                if j != []:
                    medication = j[0] + "(?x, ?y) ^"
                    rule_med = rule_med + medication

                i = i.replace(",", "")
                disease = i + "(?x) ->"
                rule_med = disease + rule_med
                rule = Imp()
                rule.set_as_rule(rule_med)
                comp_count += 1
                print(rule_med)


    onto.save(path+"/disease_ontology_trial.owl")

if __name__ == "__main__":
    create_ontology_and_rules()