from owlready2 import *
import ontor
import csv

def create_ontology():
    # https://{hostdomain}/{ontologiesRoot}/{authority}/{resourceIdentifier}.owl
    iri = "http://krr.org/disease_ontology.owl"
    fname = "./disease_ontology.owl"
    path = os.getcwd()
    ontor1 = ontor.OntoEditor(iri, fname)

    # Taxonomy: List of all [Class, Superclass], create the hierarchy of classes
    # For diseases could be: [lab_test, disease], [symptoms, disease], [physical exam, disease],
    #                       [disease, generic disease]
    with open('disease_classes.csv', newline='') as c:
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
    #print(new_classes)

    # Properties of objects including their axioms
    # [object_property (op), super-op, domain, range, functional, inverse functional, transitive, symmetric,
    # asymmetric, reflexive, irreflexive, inverse_prop]
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



    # Datatype properties including their axioms
    # [data_property (dp), super-dp, functional, domain, range, minex, minin, exact, maxin, maxex]
    #dps = [["diameter_in_cm", None, True, "pizza", "integer", None, None, None, None, None],
    #       ["weight_in_grams", None, True, "pizza", "float", None, None, None, None, None],
    #       ["description", None, False, "food", "string", None, None, None, None, None]]

    # Axioms: [class, superclass, property, inverted(bool), cardinality type, cardinality, op-object, dp-range,
    #         dp-min-ex, dp-min-in, dp-exact, dp-max-in, dp-max-ex, negated(bool), equivalence(bool)]
    #axs = [["mentalDisease", None, "isFeelingSad", None, None, None, None, None, None, None, None, None, None, None, False],
    #       ["bipolar", "mentalDisease", "hasMoodSwings", None, None, None, None, None, None, None, None, None, None, None, False],
    #       ["anorexia", "mentalDisease", "hasWeightLoss", None, None, None, None, None, None, None, None, None, None, None, False],
    #       ["autism", "mentalDisease", "hasNotSocialInteraction", None, None, None, None, None, None, None, None, None, None, None, False]]

    # Instances and their relations
    # [instance, class, property, range, range-type]
    ins = [["evaDisease", None , "isFeelingSad", None, None],
           ["williamDisease", None, "hasMoodSwings", None, None],
           ["johnDisease", None, "hasNotSocialInteraction", None, None]]


    # Add the information as lists
    ontor1.add_taxo(new_classes)
    ontor1.add_ops(new_ops)
    #ontor1.add_dps(dps)
    #ontor1.add_axioms(axs)
    #ontor1.add_instances(ins)
    ontor1.save_as(path+"/disease_ontology.owl")

def add_rules():
    onto = get_ontology('disease_ontology.owl')

    with onto:
        rule = Imp()

        class Depression(FunctionalProperty): pass
        class Anxiety(FunctionalProperty): pass
        class Irritability(FunctionalProperty): pass
        class NeuroticDisorders(EntityClass): pass

        rule.set_as_rule("Depression(?x, ?y), Anxiety(?x, ?y), "
                         "Irritability(?x, ?y) -> NeuroticDisorders(?x)")
    path = os.getcwd()
    onto.save_as(path + "/disease_ontology.owl")

if __name__ == "__main__":
    create_ontology()
    add_rules()