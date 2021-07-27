from helpers import uri_parser as up
from rdflib.namespace import RDF, OWL, RDFS, DC

def get_domain(owl_proprty, g):
    domain = []
    for rdf_property, _, _ in g.triples((owl_proprty, RDF.type, OWL.ObjectProperty)):

        for _, _, rdfs_domain in g.triples((rdf_property, RDFS.domain, None)):
            parsed_uri = up._make_fragment_uri(g, rdfs_domain)
            domain_prefix = parsed_uri['prefix']
            domain_name = parsed_uri['name']
            domain.append(f"{domain_prefix}:{domain_name}")
    return domain


def get_range(owl_proprty, g):
    range1 = []
    for rdf_property, _, _ in g.triples((owl_proprty, RDF.type, OWL.ObjectProperty)):

        for _, _, rdfs_range in g.triples((rdf_property, RDFS.range, None)):
            parsed_uri = up._make_fragment_uri(g, rdfs_range)
            range_prefix = parsed_uri['prefix']
            range_name = parsed_uri['name']
            range1.append(f"{range_prefix}:{range_name}")
    return range1


def get_super_property(owl_proprty, g):
    superproperty = []
    for rdf_property, _, _ in g.triples((owl_proprty, RDF.type, OWL.ObjectProperty)):

        for _, _, super_property in g.triples((rdf_property, RDFS.subPropertyOf, None)):
            parsed_uri = up._make_fragment_uri(g, super_property)
            super_property_prefix = parsed_uri['prefix']
            super_property_name = parsed_uri['name']
            superproperty.append(f"{super_property_prefix}:{super_property_name}")

    return superproperty


def _get_properties(g):
    properties = []
    for owl_property, _, _ in g.triples((None, RDF.type, OWL.ObjectProperty)):
        parsed_uri = up._make_fragment_uri(g, owl_property)
        property_name = parsed_uri['name']
        prefix = parsed_uri['prefix']
        label = g.label(owl_property)
        comment = g.comment(owl_property)
        domain = get_domain(owl_property, g)
        range1 = get_range(owl_property, g)
        super_property = get_super_property(owl_property, g)
        inverse_of = get_inverse_of(owl_property, g)
        characteristics = get_characteristics(owl_property, g)
        properties.append((f"{str(owl_property)}", f"{prefix}", f"{property_name}", f"{label}", f"{comment}",
                           super_property, domain, range1, inverse_of, characteristics))
    return properties


def get_characteristics(owl_proprty, g):
    characteristics = []
    for rdf_property, _, _ in g.triples((owl_proprty, RDF.type, OWL.ObjectProperty)):

        for _, _, rdf_characteristic in g.triples((rdf_property, RDF.type, None)):
            parsed_uri = up._make_fragment_uri(g, rdf_characteristic)
            characteristic_prefix = parsed_uri['prefix']
            characteristic_name = parsed_uri['name']
            if characteristic_name != 'ObjectProperty':
                if characteristic_name == 'InverseFunctionalProperty':
                    characteristics.append("Inverse Functional")
                if characteristic_name == 'FunctionalProperty':
                    characteristics.append("Functional")
                if characteristic_name == 'SymmetricProperty':
                    characteristics.append("Symmetric")
                if characteristic_name == 'AsymmetricProperty':
                    characteristics.append("Asymmetric")
                if characteristic_name == 'TransitiveProperty':
                    characteristics.append("Transitive")
                if characteristic_name == 'ReflexiveProperty':
                    characteristics.append("Reflexive")
                if characteristic_name == 'IrreflexiveProperty':
                    characteristics.append("Irreflexive")

                    # characteristics.append(f"{characteristic_name}")
    return characteristics


def get_inverse_of(owl_proprty, g):
    inverse_of = []
    for rdf_property, _, _ in g.triples((owl_proprty, RDF.type, OWL.ObjectProperty)):

        for _, _, rdfs_inverseOf in g.triples((rdf_property, OWL.inverseOf, None)):
            parsed_uri = up._make_fragment_uri(g, rdfs_inverseOf)
            inverseOf_prefix = parsed_uri['prefix']
            inverseOf_name = parsed_uri['name']
            inverse_of.append(f"{inverseOf_prefix}:{inverseOf_name}")
    return inverse_of