# rdf2adoc
A python script used to generate adoc-fragments (classes and properties) and class diagrams by analysing ontology files.
Used by the OpenXOntology project.
`python rdf2adoc.py`

## Install needed packages:
rdf2adoc uses 'rdflib' to analyze RDF triplets in ontology. Install required packages with:
```
python -m pip install -r requirements.txt
```

## Subfolder _'modules'_
This folder contains ontology file for test.

## Configuration
The *configuration yaml* shall contain the following entries:

* **`ont_inpath: "./modules/" `**
Path where the test ontology file reside
  
* **`adoc_class_outpath: "./fragments/classes/"`**
Path where the generated adoc-fragments for classes will be stored
CAUTION: The content of this path will be deleted every time rdf2adoc is started!!!

* **`adoc_prop_outpath: "./fragments/properties/"`**
Path where the generated adoc-fragments for properties will be stored
CAUTION: The content of this path will be deleted every time rdf2adoc is started!!!

* **`adoc_class_outpath: "./fragments/reference_classes/"`**
Path where the generated Reference document adoc-fragments for classes will be stored
CAUTION: The content of this path will be deleted every time rdf2adoc is started!!!

* **`adoc_prop_outpath: "./fragments/reference_properties/"`**
Path where the generated Reference document adoc-fragments for properties will be stored
CAUTION: The content of this path will be deleted every time rdf2adoc is started!!!

* **`reference_outpath: "./reference/"`**
Path where the generated Reference document will be stored
CAUTION: The content of this path will be deleted every time rdf2adoc is started!!!

* **`diag_outpath: "./webvowl_diagrams/"`**
Path where the generated WebVOWL diagrams will be stored
CAUTION: The content of this path will be deleted every time rdf2adoc is started!!!
  
* **`puml_outpath: "./fragments/puml/"`**
Path where the generated PlantUML files will be stored
CAUTION: The content of this path will be deleted every time rdf2adoc is started!!!
  
* **`logfile: "rdf2adoc.log"`**
Logging file name.

* **`plantuml_jar: "./plantuml.jar"`**
Path to the plantuml.jar for png diagram creation.

