from rdflib.namespace import RDF, OWL, RDFS


def get_stat(g):
    return "Ontology has {} statements.".format(len(g))

def get_version(g):
    version=_get_ontology_title(g) + _get_ontology_version(g)
    return version

def _get_ontology_title(g):
    for ontology in g.subjects(RDF.type, OWL.Ontology):
        for t in g.objects(ontology, RDFS.label):
            return f'{t} '
    return 'title Untitled '

def _get_ontology_version(g):
    for ontology in g.subjects(RDF.type, OWL.Ontology):
        for v in g.objects(ontology, OWL.versionInfo):
            return v
    return 'No version '




