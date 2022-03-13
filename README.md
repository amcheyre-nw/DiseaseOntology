# DiseaseOntology

## Setup

Please install the requirements in requirements.txt


## Objective & Goal

We aim to build an ontology capable of delivering psychiatric diagnoses and potential treatment options for patients given the symptoms he or she presents. Since no publicly available knowledge graph exists, this task can be split into two overarching objectives:
1. The development of data-scraping tools to build a structured medical knowledge base from online sources.
2. The creation of inference rules for each disease based on the patient's symptoms and other conditions from which we can infer certain disease diagnoses.


## Execution

1) First, run build_ontology.py.

2) Second, run owl_generation.py

3) See outputted .owl file in disease_ontology_trial.owl


### Ontology creation

To generate the csv files required for OWL file generation, simply run build_ontology.py. This will take a number of hours.

This should perform the following:

1) Produce disease_classes.csv: a file containing diseases in a hierarchial structure.
2) Produce object_props.csv: a file containing all the attributes of diseases scraped from a combination of wikipedia and DuckduckGo resources.

build_ontology.py autonomously uses the UMLS, wikipedia and DuckduckGo tools built as part of this project. The individual
functionalities of each can be seen inside ULMS_api.py, wikipedia_api.py and duckduckgo_api respectively, and examples of the
functionalities can be seen by running these individual scripts in isolation.

### OWL file generation

After the ontology csvs have been created, the file ```owl_generation.py``` must be executed, which will take the created CSVs and convert them into the OWL file named ```disease_ontology_trial.owl```. This code will create all the classes, object properties and horn clauses that then will be displayed in an ontology editor and knowledge management system. We recommend using Protege, which is the most popular and widely used ontology editor.

To start using the file, it just needs uploading to the ontology editor and everything will be displayed and ready to use.
