# DiseaseOntology

## Objective & Goal 

We aim to build an ontology capable of delivering psychiatric diagnoses and potential treatment options for patients given the symptoms he or she presents. Since no publicly available knowledge graph exists, this task can be split into two overarching objectives:
1. The development of data-scraping tools to build a structured medical knowledge base from online sources.
2. The creation of inference rules for each disease based on the patient's symptoms and other conditions from which we can infer certain disease diagnoses.

## Execution

### Ontology creation

XXXX

### OWL file generation

After having created the ontology, it generates two CSV outputs ```disease_classes.csv``` and ```object_props.csv```. The file ```owl_generation.py``` have to be executed in the main, which will take the created CSVs and convert them into the OWL file that then will be uploaded to Protege.

The output file ```disease_ontology.owl``` is the one that have to be uploaded in Protege to be able to start reasoning with it.



