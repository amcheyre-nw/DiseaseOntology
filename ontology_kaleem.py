from owlready2 import *
import ontor

def create_ontology():
    # https://{hostdomain}/{ontologiesRoot}/{authority}/{resourceIdentifier}.owl
    iri = "http://example.org/disease_ontology_kaleem.owl"
    fname = "./disease_ontology_kaleem.owl"
    ontor1 = ontor.OntoEditor(iri, fname)
    classes = [["Psychiactric Disroders", None], \
               ["Psychotic Disorders", "Psychiactric Disroders"], \
               ["Schizophrenia", "Psychotic Disorders"], \
               ["Schizophreniform Disorder", "Psychotic Disorders"], \
               ["Brief Psychotic Disorder", "Psychotic Disorders"], \
               ["Schizoaffective Disorder", "Psychotic Disorders"], \
               ["Delusional Disorder", "Psychotic Disorders"], \
               ["symptoms or signs", "Schizophrenia"], \
               ["lab_tests", "Schizophrenia"], \
               ["physical_exam", "Schizophrenia"], \
               ["pharmacologic treatment", "Schizophrenia"], \
               ["non-phamacologic treatment", "Schizophrenia"], \
               ["symptoms or signs", "Schizophreniform Disorder"], \
               ["lab_tests", "Schizophreniform Disorder"], \
               ["physical_exam", "Schizophreniform Disorder"], \
               ["pharmacologic treatment", "Schizophreniform Disorder"], \
               ["non-phamacologic treatment", "Schizophreniform Disorder"], \
               ["symptoms or signs", "Brief Psychotic Disorder"], \
               ["lab_tests", "Brief Psychotic Disorder"], \
               ["physical_exam", "Brief Psychotic Disorder"], \
               ["pharmacologic treatment", "Brief Psychotic Disorder"], \
               ["non-phamacologic treatment", "Brief Psychotic Disorder"], \
               ["symptoms or signs", "Schizoaffective Disorder"], \
               ["lab_tests", "Schizoaffective Disorder"], \
               ["physical_exam", "Schizoaffective Disorder"], \
               ["pharmacologic treatment", "Schizoaffective Disorder"], \
               ["non-phamacologic treatment", "Schizoaffective Disorder"], \
               ["symptoms or signs", "Delusional Disorder"], \
               ["lab_tests", "Delusional Disorder"], \
               ["physical_exam", "Delusional Disorder"], \
               ["pharmacologic treatment", "Delusional Disorder"], \
               ["non-phamacologic treatment", "Delusional Disorder"]]

    # Properties of objects including their axioms
    # [object_property (op), super-op, domain, range,functional, inverse functional, transitive, symmetric,
    # asymmetric, reflexive, irreflexive, inverse_prop]
    ops = [["likes", None, "human", None, False, False, False, False, False, False, False, None]]

    # Datatype properties including their axioms
    # [data_property (dp), super-dp, functional, domain, range, minex, minin, exact, maxin, maxex]
    dps = [["diameter_in_cm", None, True, "pizza", "integer", None, None, None, None, None],
           ["weight_in_grams", None, True, "pizza", "float", None, None, None, None, None],
           ["description", None, False, "food", "string", None, None, None, None, None]]

    # Axioms: [class, superclass, property, inverted(bool), cardinality type, cardinality, op-object, dp-range,
    #         dp-min-ex, dp-min-in, dp-exact, dp-max-in, dp-max-ex, negated(bool), equivalence(bool)]
    axs = [["human", None, "likes", None, "some", None, "food", None, None, None, None, None, None, None, False]]

    # Instances and their relations
    # [instance, class, property, range, range-type]
    ins = [["John", "vegetarian", None, None, None], \
           ["His_pizza", "margherita", None, None, None], \
           ["John", "vegetarian", "likes", "His_pizza", None]]

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

    ontor1.save_as(path + "/disease_ontology.owl")

    # Visualize a graph
    # ontor1.visualize(classes=["human", "pizza"], properties=["likes", "diameter_in_cm"], focusnode="John", radius=2)


if __name__ == "__main__":
    create_ontology()