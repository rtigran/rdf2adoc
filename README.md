# rdf2adoc

A python script used to generate adoc-fragments (classes and properties) and class diagrams by analysing ontology files.
Used by the OpenXOntology project.
`python rdf2adoc.py`

## Subfolder _'modules'_
This folder contains ontology for test.

## Configuration
The *configuration yaml* shall contain the following entries:

* **`ont_inpath: "./modules/corePlus20210722.ttl" `**
Path where the ontology file
  
* **`adoc_prop_outpath: "./fragments/properties/"`**
Path where the generated adoc-fragments for properties will be stored
CAUTION: The content of this path will be deleted every time rdf2adoc is started!!!

* **`adoc_prop_outpath: "./fragments/properties/"`**
Path where the generated adoc-fragments for properties will be stored
CAUTION: The content of this path will be deleted every time rdf2adoc is started!!!

* **`diag_outpath: "./fragments/diagrams/"`**
Path where the generated class diagrams will be stored
CAUTION: The content of this path will be deleted every time rdf2adoc is started!!!
  
* **`puml_inpath: "./fragments/puml/"`**
Path where the generated PlantUML files will be stored
CAUTION: The content of this path will be deleted every time rdf2adoc is started!!!
  
*  **`logfile: "rdf2adoc.log"`**
Logging file name.

* **`plantuml_jar: "./plantuml.jar"`**
Path to the plantuml.jar for png diagram creation.

Note: rdf2adoc uses 'rdflib' to analyze RDF triplets in ontology. You may have to install rdflib using `pip install rdflib`
