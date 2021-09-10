from rdflib import Graph
import os


def _add_reference_class_adoc(path, prefix):
    reference_adoc = ''
    if os.path.exists(path):
        files = []
        for filename in os.listdir(path):
            files.append(filename)
        files.sort()
        for filename in files:
            #fullfilename = os.path.join(path, filename)
            if filename.startswith(prefix):
                reference_adoc += (f"include::../reference_classes/{filename}[leveloffset=+1]\n\n")
    return reference_adoc

def _add_reference_prop_adoc(path, prefix):
    reference_adoc = ''
    if os.path.exists(path):
        files = []
        for filename in os.listdir(path):
            files.append(filename)
        files.sort()
        for filename in files:
            #fullfilename = os.path.join(path, filename)
            if filename.startswith(prefix):
                reference_adoc += (f"include::../reference_properties/{filename}[leveloffset=+1]\n\n")
    return reference_adoc

def _add_reference_links(path, prefix):
    reference_adoc = ''
    reference_adoc += "[%hardbreaks] \n"
    if os.path.exists(path):
        files = []
        for filename in os.listdir(path):
            files.append(filename)
        files.sort()
        for filename in files:
            if filename.startswith(prefix):
                filename = filename.split('_')[1].split('.')[0]
                reference_adoc += (f"link:#{filename}[{filename}] \n" )
    reference_adoc += "\n"
    return reference_adoc

def _get_puml_properties(class_item, classes):
    plant_uml = f'Card {class_item} #F0F8FF [\n'
    plant_uml += f'{class_item}\n'
    for class_uri, _, class_name, _, _, _, _, properties, _ in classes:
        if class_item == class_name:
            if properties != '':
                plant_uml += '----\n'
                plant_uml += f'{properties}'
    plant_uml += ']\n'
    return plant_uml

def _write_class_file(class_file_name, owl_class, prefix, class_name, class_file_header, version, superclass, restrictions, disjoints, comments):
    with open(class_file_name, 'w', encoding="utf-8") as fobj:

        class_adoc = (f"// This file was created automatically by {version}.\n")
        class_adoc += (f"// DO NOT EDIT!\n\n")
        # class_adoc += (f"= {class_name}\n\n")
        class_adoc += (f"//Include information from owl files\n\n")
        class_adoc += (f"[#{class_name}]\n")
        class_adoc += class_file_header
        class_adoc += '[plantuml, svg]\n'
        class_adoc += '....\n'
        class_adoc += (f"include::../puml/{prefix}_{class_name}.plantuml[leveloffset=+1] \n")
        class_adoc += '....\n\n'
        class_adoc += ('|===\n|Element |Description\n\n')
        class_adoc += (f"|Type\n|Class\n\n")
        class_adoc += (f"|Name\n|{class_name}\n\n")
        class_adoc += (f"|IRI\n|{owl_class}\n\n")

        # if label != '': class_adoc += (f"|Label\n|{label}\n\n")

        for superclass_item in superclass:
            class_adoc += (f"|Subclass of\n|{superclass_item}\n\n")
        if restrictions != []:
            for restrictions_item in restrictions:
                class_adoc += (
                    f"|Restriction\n|{restrictions_item[0]} {restrictions_item[1]} {restrictions_item[2]}\n\n")
        if disjoints != []:
            for disjoints_item in disjoints:
                class_adoc += (f"|Disjoint with\n|{disjoints_item}\n\n")

        if comments != []:
            class_adoc += (f"|Comments\n|")
            for comments_item in comments:
                if comments_item.startswith("DEF") or comments_item.startswith("USAGE") or comments_item.startswith(
                        "EXAMPLE"):
                    class_adoc += (f"{comments_item}\n\n")
                if comments_item.startswith("HQDM"):
                    term = comments_item.removeprefix("HQDM ")
                    class_adoc += (
                        f"link:http://www.informationjunction.co.uk/hqdm_framework/hqdm_framework/lexical/{term}.htm[Reference to {comments_item}] \n\n")
        class_adoc += ("|===")

        fobj.write(class_adoc)

def _write_prop_file(prop_file_name, property_uri, prefix, property_name, prop_file_header, version,
                                     subPropertyOf, domain, range1, inverse_of, characteristics, comments):
    with open(prop_file_name, 'w', encoding="utf-8") as fobj:

        prop_adoc = (f"// This file was created automatically by {version}.\n// DO NOT EDIT!\n\n")
        # prop_adoc += (f"= {property_name}\n\n")
        prop_adoc += (f"//Include information from owl files\n\n")

        prop_adoc += (f"[#{property_name}]\n")
        prop_adoc += prop_file_header
        prop_adoc += ('|===\n|Element |Description\n\n')
        prop_adoc += (f"|Type\n|ObjectProperty\n\n")
        prop_adoc += (f"|Name\n|{property_name}\n\n")
        prop_adoc += (f"|IRI\n|{property_uri}\n\n")
        if subPropertyOf != []:
            for subPropertyOf_item in subPropertyOf:
                prop_adoc += (f"|Subproperty of\n|{subPropertyOf_item}\n\n")

        if domain != []:
            for domain_item in domain:
                prop_adoc += (f"|Has domain\n|{domain_item}\n\n")
        if range1 != []:
            for range1_item in domain:
                prop_adoc += (f"|Has range\n|{range1_item}\n\n")
        if inverse_of != []:
            for inverse_of_item in inverse_of:
                prop_adoc += (f"|Inverse\n|{inverse_of_item}\n\n")
        if characteristics != []:
            for characteristics_item in characteristics:
                prop_adoc += (f"|Characteristic\n|{characteristics_item}\n\n")

        # if label != '': prop_adoc += (f"|Label\n|{label}\n\n")

        if comments != []:
            prop_adoc += (f"|Comments\n|")
            for comments_item in comments:
                if comments_item.startswith("DEF") or comments_item.startswith("USAGE") or comments_item.startswith(
                        "EXAMPLE"):
                    prop_adoc += (f"{comments_item}\n\n")
                if comments_item.startswith("HQDM"):
                    term = comments_item.removeprefix("HQDM ")
                    prop_adoc += (f"[Equivalent to {comments_item}] \n\n")

        prop_adoc += ("|===")

        fobj.write(prop_adoc)