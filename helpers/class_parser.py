from helpers import uri_parser as up
from rdflib.namespace import RDF, OWL, RDFS, DC

def get_class_definition(g, owl_class):
    parsed_uri = up._make_fragment_uri(g, owl_class)
    class_name = parsed_uri['name']
    prefix = parsed_uri['prefix']
    #label = g.label(owl_class)
    comments = get_comments(owl_class,g)
    superclass = get_superclass(owl_class, g)
    restrictions = get_restrictions(owl_class, g)
    disjoints = get_disjoints(owl_class, g)
    properties = get_properties(owl_class, g)
    subclass=get_subclass(owl_class, g)
    return (owl_class, f"{prefix}", f"{class_name}", comments, superclass, restrictions, disjoints, properties, subclass)


def get_classes(g):
    classes = []
    for owl_class, _, _ in g.triples((None, RDF.type, OWL.Class)):
        parsed_uri = up._make_fragment_uri(g, owl_class)
        owl_class_namespace = parsed_uri['namespace']

        if owl_class_namespace !='':
            classes.append(get_class_definition(g, owl_class))
                #for _, _, equivalent_class in g.triples((owl_class, OWL.equivalentClass, None)):
                #    classes.append(get_class_definition(g, equivalent_class))
    return classes


def get_superclass(owl_class, g):
    superclass = []

    for _, _, super_class in g.triples((owl_class, RDFS.subClassOf, None)):

        owl_restriction_bool = _is_class_type_owl_restriction(super_class, g)
        if not owl_restriction_bool:
            parsed_uri = up._make_fragment_uri(g, super_class)
            super_class_prefix = parsed_uri['prefix']
            super_class_name = parsed_uri['name']
            superclass.append(f"{super_class_name}")

    if superclass == []:
        superclass = ['Thing']

    return superclass


def _is_class_type_owl_restriction(super_class, g):
    for _, _, class_type in g.triples((super_class, RDF.type, OWL.Restriction)):
        return True
    return False


def _convert_restriction(G, restriction_bn):
    restriction=[]
    prop = None
    card = None
    cls = None
    card_cls = None

    for p2, o2 in G.predicate_objects(subject=restriction_bn):
        if p2 != RDF.type:
            if p2 == OWL.onProperty:
                prop = up._get_last_segment_of_uri(o2)
            elif p2 == OWL.onClass:
                cls = up._get_last_segment_of_uri(o2)
            elif p2 in [
                OWL.cardinality,
                OWL.qualifiedCardinality,
                OWL.minCardinality,
                OWL.minQualifiedCardinality,
                OWL.maxCardinality,
                OWL.maxQualifiedCardinality,
            ]:
                if p2 in [OWL.minCardinality, OWL.minQualifiedCardinality]:
                    card = "min"
                elif p2 in [OWL.maxCardinality, OWL.maxQualifiedCardinality]:
                    card = "max"
                elif p2 in [OWL.cardinality, OWL.qualifiedCardinality]:
                    card = "exactly"
                card = '**{}** **{}**'.format(card, str(o2))
            elif p2 in [OWL.allValuesFrom, OWL.someValuesFrom]:
                if p2 == OWL.allValuesFrom:
                    card = "only"
                else:  # p2 == OWL.someValuesFrom
                    card = "some"

                card = '**{}**'.format(card)
                card_cls = '{}'.format(up._get_last_segment_of_uri(o2))
            elif p2 == OWL.hasValue:
                card = '**value** {}'.format(up._get_last_segment_of_uri(o2))

    restriction = [prop, card, card_cls] if card_cls is not None else [prop, card, cls]
    #restriction = restriction.append(cls) if cls is not None else restriction
    
    return restriction


def get_restrictions(owl_class, g):
    restrictions = []

    for _, _, super_class in g.triples((owl_class, RDFS.subClassOf, None)):

        owl_restriction_bool = _is_class_type_owl_restriction(super_class, g)

        if owl_restriction_bool:
            restriction = _convert_restriction(g, super_class)
            restrictions.append(restriction)

    return restrictions

def get_disjoints(owl_class, g):
    disjoints = []
    for _, _, disjoint_class in g.triples((owl_class, OWL.disjointWith, None)):
        parsed_uri = up._make_fragment_uri(g, disjoint_class)
        disjoint_class_prefix = parsed_uri['prefix']
        disjoint_class_name = parsed_uri['name']
        disjoints.append(f"{disjoint_class_name}")
    return disjoints

def get_properties(owl_class, g):
    plant_uml = ''

    for rdf_property, _, _ in g.triples((None, RDF.type, OWL.ObjectProperty)):
        for _, _, rdfs_range in g.triples((rdf_property, RDFS.range, None)):
            for _, _, rdfs_domain in g.triples((rdf_property, RDFS.domain, None)):
                if rdfs_domain ==owl_class:
                    parsed_rdfs_range = up._make_fragment_uri(g, rdfs_range)
                    parsed_rdfs_range_name = parsed_rdfs_range['name']

                    parsed_rdfs_rdf_property = up._make_fragment_uri(g, rdf_property)
                    parsed_rdfs_rdf_property_name = parsed_rdfs_rdf_property['name']

                    plant_uml += f'- {parsed_rdfs_rdf_property_name} : {parsed_rdfs_range_name} \n'
                break
            break
    return plant_uml

def get_subclass(owl_class, g):
    subclass = []
    for sub_class, _,_  in g.triples((None, RDFS.subClassOf, owl_class)):
        owl_restriction_bool = _is_class_type_owl_restriction(sub_class, g)
        if not owl_restriction_bool:
            parsed_uri = up._make_fragment_uri(g, sub_class)
            subclass_prefix = parsed_uri['prefix']
            sub_class_name = parsed_uri['name']
            subclass.append(f"{sub_class_name}")
    return subclass

def get_comments(owl_class, g):
    comments = []
    for _, _, comment in g.triples((owl_class, RDFS.comment, None)):
        comments.append(f"{comment}")
        comments.sort(key=lambda s:s.startswith("HQDM"))
    return comments