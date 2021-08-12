from rdflib import Graph
import os
from os import listdir
from os.path import isfile, join
import subprocess
from helpers import class_parser as cp
from helpers import property_parser as pp
from helpers import ont_version as v
from helpers import filehelper as f
from datetime import datetime


class RDF2adoc:
    def __init__(self, filepath : str, class_outpath : str, prop_outpath : str, puml_outpath : str, format='turtle'):
        self.__filepath = filepath
        self.__class_outpath = class_outpath
        self.__prop_outpath = prop_outpath
        self.__puml_outpath = puml_outpath

        self.g = Graph().parse(self.__filepath, format=format)
        self.__version=v.get_version(self.g)
        self.__stat=v.get_stat(self.g)
        self.__classes = cp.get_classes(self.g)
        self.__properties = pp.get_properties(self.g)

    @property
    def version(self):
        return self.__version
    @property
    def stat(self):
        return self.__stat

    def gen_class_adoc(self):
        if self.__classes:
            f.logprint("Ontology has {} classes.".format(len(self.__classes)))
            self.__classes.sort()
            for owl_class, \
                prefix, \
                class_name, \
                label, \
                comment, \
                superclass, \
                restrictions, \
                disjoints, \
                properties, \
                subclass \
                    in self.__classes:
                with open(f"{self.__class_outpath}{class_name}.adoc", 'w', encoding="utf-8") as fobj:

                    class_adoc = (f"// This file was created automatically by {self.__version}.\n// DO NOT EDIT!\n\n")
                    class_adoc += (f"= {class_name}\n\n")
                    class_adoc += (f"//Include information from owl files\n\n")
                    class_adoc += (f"The following model provides an overview of {class_name}\n\n")
                    class_adoc += (f"//include::{self.__puml_outpath}/{class_name}.plantuml[] \n\n")
                    class_adoc += ('|===\n|Element |Description\n\n')
                    class_adoc += (f"|Type\n|Class\n\n")
                    class_adoc += (f"|Name\n|{class_name}\n\n")
                    class_adoc += (f"|IRI\n|{owl_class}\n\n")

                    if label != '': class_adoc += (f"|Label\n|{label}\n\n")

                    for superclass_item in superclass:
                        class_adoc += (f"|Subclass of\n|{superclass_item}\n\n")
                    if restrictions != []:
                        for restrictions_item in restrictions:
                            class_adoc += (f"|Restriction\n|{restrictions_item[0]} {restrictions_item[1]} {restrictions_item[2]}\n\n")
                    if disjoints != []:
                        for disjoints_item in disjoints:
                            class_adoc += (f"|Disjoint with\n|{disjoints_item}\n\n")

                    if comment != '': class_adoc += (f"|Comment\n|{comment}\n\n")
                    class_adoc += ("|===")

                    fobj.write(class_adoc)

    def gen_prop_adoc(self):
        if self.__properties:
            f.logprint("Ontology has {} properties.".format(len(self.__properties)))
            self.__properties.sort()
            for property_uri, \
                prefix, \
                property_name, \
                label, comment, \
                subPropertyOf, \
                domain, \
                range1, \
                inverse_of, \
                characteristics \
                    in self.__properties:
                with open(f"{self.__prop_outpath}{property_name}.adoc", 'w', encoding="utf-8") as fobj:

                    prop_adoc=(f"// This file was created automatically by {self.__version}.\n// DO NOT EDIT!\n\n")
                    prop_adoc += (f"= {property_name}\n\n")
                    prop_adoc += (f"//Include information from owl files\n\n")
                    prop_adoc += (f"The following model provides an overview of {property_name}\n\n")
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

                    if label != '': prop_adoc += (f"|Label\n|{label}\n\n")
                    if comment != '': prop_adoc += (f"|Comment\n|{comment}\n\n")

                    prop_adoc += ("|===")

                    fobj.write(prop_adoc)

    def gen_diag(self):
        try:
            if f.get_plantuml_jar():
                f.logprint("plantuml jar started at ", datetime.now().strftime("%H:%M:%S"))
                path=self.__puml_outpath
                for filename in os.listdir(path):
                    diag_filename = os.path.join(path, filename)
                    if os.path.isfile(diag_filename):
                        subprocess.run(["java", "-jar", f.get_plantuml_jar(), diag_filename, "-o", f.get_diag_outpath()])
                f.logprint("plantuml jar finished at ",datetime.now().strftime("%H:%M:%S"))
        except:
            f.logprint("no plantuml.jar defined or found")

    def gen_puml(self):
        if self.__classes:
            self.__classes.sort()
            path=self.__puml_outpath
            for class_uri,\
                prefix, \
                class_name, \
                label, \
                comment, \
                superclass, \
                restrictions, \
                disjoints, \
                properties, \
                subclass \
                    in self.__classes:
                puml_filename = os.path.join(path, class_name)
                with open(f"{puml_filename}.plantuml", 'w', encoding="utf-8") as fobj:
                    plant_uml = '@startuml\n'
                    plant_uml += f'Title {class_name} \n'
                    plant_uml += f'Card {class_name} #F0F8FF [\n'
                    plant_uml += f'{class_name}\n'
                    if properties != '':
                        plant_uml += '----\n'
                        plant_uml += f'{properties}'
                    plant_uml += ']\n'
                    for superclass_item in superclass:
                        plant_uml +=self._get_puml_properties(superclass_item)
                        plant_uml += f'{superclass_item} --|> {class_name}  #00008B \n'
                    for subclass_item in subclass:
                        plant_uml += self._get_puml_properties(subclass_item)
                        plant_uml += f'{class_name} --|> {subclass_item}  #00008B \n'
                    plant_uml += '@enduml'

                    fobj.write(plant_uml)

    def _get_puml_properties(self, class_item):
        plant_uml = f'Card {class_item} #F0F8FF [\n'
        plant_uml += f'{class_item}\n'
        for class_uri, _, class_name, _, _, _, _, _, properties, _ in self.__classes:
            if class_item == class_name:
                if properties != '':
                    plant_uml += '----\n'
                    plant_uml += f'{properties}'
        plant_uml += ']\n'
        return plant_uml