from owlready2 import *
import ontor

def create_ontology():
    # https://{hostdomain}/{ontologiesRoot}/{authority}/{resourceIdentifier}.owl
    iri = "http://example.org/disease_ontology_kaleem.owl"
    fname = "./disease_ontology_kaleem.owl"
    path = os.getcwd()
    ontor1 = ontor.OntoEditor(iri, fname)
    classes = [["Psychiactric_Disroders", None], \
               ["Psychotic_Disorders", "Psychiactric_Disorders"], \
               ["Schizophrenia", "Psychotic_Disorders"], \
               ["Schizophreniform_Disorder", "Psychotic_Disorders"], \
               ["Brief_Psychotic_Disorder", "Psychotic_Disorders"], \
               ["Schizoaffective_Disorder", "Psychotic_Disorders"], \
               ["Delusional_Disorder", "Psychotic_Disorders"], \
               ["Mood_Disorders", None],\
               ["Mood_Episodes", "Mood_Disorders"], \
               ["Depressive_Disorders", "Mood_Disorders"], \
               ["Bipolar_Disorders", "Mood_Disorders"], \
               ["Anxiety_Disorders", None], \
               ["Panic_Disorder", "Anxiety_Disorders"], \
               ["Agoraphobia", "Anxiety_Disorders"], \
               ["Generalized_Anxiety_Disorder", "Anxiety_Disorders"], \
               ["Phobic_Disorders", "Anxiety_Disorders"], \
               ["Symptoms_or_Signs", None], \
               ["Physical_Exam", None], \
               ["Lab_or_Test_Result", None], \
               ["Treatment", None], \
               ["Pharmacological_Intervention", "Treatment"],\
               ["Non_Pharmacological_Intervention", "Treatment"]]

    # Properties of objects including their axioms
    # [object_property (op), super-op, domain, range,functional, inverse functional, transitive, symmetric,
    # asymmetric, reflexive, irreflexive, inverse_prop]
    ops = [[]]

    # Datatype properties including their axioms
    # [data_property (dp), super-dp, functional, domain, range, minex, minin, exact, maxin, maxex]
    dps = [[]]

    # Axioms: [class, superclass, property, inverted(bool), cardinality type, cardinality, op-object, dp-range,
    #         dp-min-ex, dp-min-in, dp-exact, dp-max-in, dp-max-ex, negated(bool), equivalence(bool)]
    axs = [[]]

    # Instances and their relations
    # [instance, class, property, range, range-type]
    ins = [[]]

    # Import information from CSV and JSON files (not working yet)
    # ontor1.add_taxo(ontor.load_csv(path+"/taxo.csv"))
    # ontor1.add_ops(ontor.load_json(path+"/props.json")["op"])
    # ontor1.add_dps(ontor.load_json(path+"/props.json")["dp"])
    # ontor1.add_axioms(ontor.load_csv(path+"/class_axioms.csv"))

    # Add the information as lists
    ontor1.add_taxo(classes)
    ontor1.add_ops(ops)
    ontor1.add_dps(dps)
    ontor1.add_axioms(axs)
    ontor1.add_instances(ins)

    ontor1.save_as(path + "/disease_ontology_kaleem.owl")

    # Visualize a graph
    # ontor1.visualize(classes=["human", "pizza"], properties=["likes", "diameter_in_cm"], focusnode="John", radius=2)


if __name__ == "__main__":
    create_ontology()
