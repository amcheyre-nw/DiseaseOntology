# DiseaseOntology

## Objective & Goal 

We aim to build an ontology capable of delivering psychiatric diagnoses and potential treatment options for patients given the symptoms he or she presents. Since no publicly available knowledge graph exists, this task can be split into two overarching objectives:
1. The development of data-scraping tools to build a structured medical knowledge base from online sources.
2. The creation of inference rules for each disease based on the patient's symptoms and other conditions from which we can infer certain disease diagnoses.

## Execution

### Ontology creation

XXXX

### OWL file generation

After the ontology is created, the file ```owl_generation.py``` have to be executed, which will take the created CSVs and convert them into the OWL file. This code will create all the classes, object properties and horn clauses that then will be displayed in an open source ontology editor and knowledge management system. We recommend using Protege, which is the most popular and widely used ontology editor.

To start using the file, it just have to be uploaded to the ontology editor and everything will be displayed and ready to use.
