from rdflib import Graph
import os
from os import listdir
from os.path import isfile, join
import subprocess
from helpers import class_parser as cp
from helpers import property_parser as pp
from helpers import ont_version as v
from helpers import filehelper as f
from helpers import fragments_parser as fr
from datetime import datetime
from helpers.color import COLOR
import random


class RDF2adoc:
    def __init__(self, filepath : str, class_outpath : str, reference_class_outpath : str, prop_outpath : str, reference_prop_outpath : str, puml_outpath : str, reference_outpath : str, format='turtle'):
        self.__filepath = filepath
        self.__class_outpath = class_outpath
        self.__reference_class_outpath = reference_class_outpath
        self.__prop_outpath = prop_outpath
        self.__reference_prop_outpath = reference_prop_outpath
        self.__puml_outpath = puml_outpath
        self.__reference_outpath = reference_outpath

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
                comments, \
                superclass, \
                restrictions, \
                disjoints, \
                properties, \
                subclass \
                    in self.__classes:
                class_file_name=f"{self.__class_outpath}{prefix}_{class_name}.adoc"
                reference_class_file_name = f"{self.__reference_class_outpath}{prefix}_{class_name}.adoc"

                class_file_header=(f"**OWL definition of {class_name}**\n\n")
                class_file_header += (f"The following model provides an overview of {class_name}:\n\n")
                reference_class_file_header = (f"==== {class_name}\n\n")

                fr._write_class_file(class_file_name, owl_class, prefix, class_name, class_file_header, self.__version, superclass, restrictions, disjoints, comments)
                fr._write_class_file(reference_class_file_name, owl_class, prefix, class_name, reference_class_file_header, self.__version, superclass, restrictions, disjoints, comments)

    def gen_prop_adoc(self):
        if self.__properties:
            f.logprint("Ontology has {} properties.".format(len(self.__properties)))
            self.__properties.sort()
            for property_uri, \
                prefix, \
                property_name, \
                comments, \
                subPropertyOf, \
                domain, \
                range1, \
                inverse_of, \
                characteristics \
                    in self.__properties:

                prop_file_name = f"{self.__prop_outpath}{prefix}_{property_name}.adoc"
                reference_prop_file_name = f"{self.__reference_prop_outpath}{prefix}_{property_name}.adoc"

                prop_file_header = (f"**OWL definition of {property_name}**\n\n")
                prop_file_header += (f"The following model provides an overview of {property_name}:\n\n")
                reference_prop_file_header = (f"==== {property_name}\n\n")

                fr._write_prop_file(prop_file_name, property_uri, prefix, property_name, prop_file_header, self.__version,
                                     subPropertyOf, domain, range1, inverse_of, characteristics, comments)
                fr._write_prop_file(reference_prop_file_name, property_uri, prefix, property_name,
                                     reference_prop_file_header, self.__version, subPropertyOf, domain, range1, inverse_of, characteristics,
                                     comments)

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
                comment, \
                superclass, \
                restrictions, \
                disjoints, \
                properties, \
                subclass \
                    in self.__classes:
                puml_name=prefix+'_'+class_name
                puml_filename = os.path.join(path, puml_name)
                with open(f"{puml_filename}.plantuml", 'w', encoding="utf-8") as fobj:
                    card = []
                    plant_uml = '@startuml\n'
                    plant_uml += 'scale max 350 height \n'
                    #plant_uml = f'Title {class_name} \n'
                    card.append(class_name)
                    plant_uml += f'Card {class_name} #F0F8FF [\n'
                    plant_uml += f'{class_name}\n'
                    if properties != '':
                        plant_uml += '----\n'
                        plant_uml += f'{properties}'
                    plant_uml += ']\n'

                    if restrictions != []:
                        x=0
                        for restrictions_item in restrictions:
                            color=COLOR[x]
                            if restrictions_item[2] not in card:
                                card.append(restrictions_item[2])
                                plant_uml += fr._get_puml_properties(restrictions_item[2], self.__classes)
                            plant_uml += f'{class_name} ..> {restrictions_item[2]} {color} : {restrictions_item[0]} {restrictions_item[1]}  \n'
                            x=x+1
                            if x>12:
                                x=0

                    for superclass_item in superclass:
                        if superclass_item not in card:
                            card.append(superclass_item)
                            plant_uml +=fr._get_puml_properties(superclass_item, self.__classes)
                        plant_uml += f'{superclass_item} --|> {class_name}  #00008B \n'

                    for subclass_item in subclass:
                        if subclass_item not in card:
                            card.append(subclass_item)
                            plant_uml += fr._get_puml_properties(subclass_item, self.__classes)
                        plant_uml += f'{class_name} --|> {subclass_item}  #00008B \n'
                    plant_uml += '@enduml'

                    fobj.write(plant_uml)

    def gen_reference(self):
        reference_adoc=''
        path=self.__reference_outpath
        reference_filename = os.path.join(path, 'Reference')
        with open(f"{reference_filename}.adoc", 'w', encoding="utf-8") as fobj:
            reference_adoc += (f"// This file was created automatically by {self.__version}.\n")
            reference_adoc += (f"// DO NOT EDIT!\n\n")
            reference_adoc += (f"= OpenXOntology Model Reference\n")
            reference_adoc +=':encoding: utf-8 \n'
            reference_adoc +=':lang: en \n'
            reference_adoc +=':table-stripes: even \n'
            reference_adoc +=':toc: \n'
            reference_adoc +=':toc-placement!: \n'
            reference_adoc +=':toclevels: 2 \n'
            reference_adoc +=':sectnumlevels: 4 \n'
            reference_adoc +=':sectanchors: \n'
            reference_adoc +=':figure-id: 0 \n'
            reference_adoc +=':table-id: 0 \n'
            reference_adoc +=':req-id: 0 \n'
            reference_adoc +=':rec-id: 0 \n'
            reference_adoc +=':per-id: 0 \n'
            reference_adoc +=':xrefstyle: short \n'
            reference_adoc +=':chapter-refsig: Clause \n'
            reference_adoc +=':idprefix: \n'
            reference_adoc +=':idseparator: \n\n'
            reference_adoc +='<<< \n'
            reference_adoc +='Version Information:: \n'
            reference_adoc += (f"{self.__version}\n\n")
            reference_adoc +='toc::[] \n'
            reference_adoc +='<<< \n'
            reference_adoc +='\n'
            reference_adoc +=':sectnums!: \n\n'
            reference_adoc += (f"== Core Ontology Module\n\n")

            reference_adoc += (f"=== Classes\n\n")

            reference_adoc +=fr._add_reference_links(self.__reference_class_outpath, 'Core')
            reference_adoc +=fr._add_reference_adoc(self.__reference_class_outpath, 'Core')

            reference_adoc += (f"=== Properties\n\n")
            reference_adoc += fr._add_reference_links(self.__reference_prop_outpath, 'Core')
            reference_adoc += fr._add_reference_adoc(self.__reference_prop_outpath, 'Core')

            reference_adoc += (f"== Domain Ontology Module\n\n")

            reference_adoc += (f"=== Classes\n\n")
            reference_adoc += fr._add_reference_links(self.__reference_class_outpath, 'Domain')
            reference_adoc += fr._add_reference_adoc(self.__reference_class_outpath, 'Domain')

            reference_adoc += (f"=== Properties\n\n")
            reference_adoc += fr._add_reference_links(self.__reference_prop_outpath, 'Domain')
            reference_adoc += fr._add_reference_adoc(self.__reference_prop_outpath, 'Domain')

            fobj.write(reference_adoc)



