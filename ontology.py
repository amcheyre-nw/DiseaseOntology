from owlready2 import *
import ontor

def create_ontology():
    # https://{hostdomain}/{ontologiesRoot}/{authority}/{resourceIdentifier}.owl
    iri = "http://example.org/disease_ontology.owl"
    fname = "./disease_ontology.owl"
    ontor1 = ontor.OntoEditor(iri, fname)
    classes = [["human", None],\
               ["vegetarian", "human"],\
               ["food", None],\
               ["pizza", "food"],\
               ["pizza_base", "food"],\
               ["pizza_topping", "food"],\
               ["vegetarian_pizza", "pizza"],\
               ["margherita", "vegetarian_pizza"]]
    ops = [["likes", None, "human", None, False, False, False, False, False, False, False, None]]
    dps = [["diameter_in_cm", None, True, "pizza", "integer", None, None, None, None, None],
           ["weight_in_grams", None, True, "pizza", "float", None, None, None, None, None],
           ["description", None, False, "food", "string", None, None, None, None, None]]
    axs = [["human", None, "likes", None, "some", None, "food", None, None, None, None, None, None, None, False]]
    ins = [["John", "vegetarian", None, None, None],\
           ["His_pizza", "margherita", None, None, None],\
           ["John", "vegetarian", "likes", "His_pizza", None]]

    ontor1.add_taxo(classes)
    ontor1.add_ops(ops)
    ontor1.add_dps(dps)
    ontor1.add_axioms(axs)
    ontor1.add_instances(ins)
    path = os.getcwd()
    ontor1.save_as(path+"/disease_ontology.owl")

    # Visualize a graph
    #ontor1.visualize(classes=["human", "pizza"], properties=["likes", "diameter_in_cm"], focusnode="John", radius=2)

if __name__ == "__main__":
    create_ontology()