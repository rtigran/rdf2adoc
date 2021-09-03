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
    def __init__(self, filepath : str, class_outpath : str, prop_outpath : str, puml_outpath : str, appendix_outpath : str, format='turtle'):
        self.__filepath = filepath
        self.__class_outpath = class_outpath
        self.__prop_outpath = prop_outpath
        self.__puml_outpath = puml_outpath
        self.__appendix_outpath = appendix_outpath

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

                with open(f"{self.__class_outpath}{prefix}_{class_name}.adoc", 'w', encoding="utf-8") as fobj:

                    class_adoc = (f"// This file was created automatically by {self.__version}.\n")
                    class_adoc += (f"// DO NOT EDIT!\n\n")
                    #class_adoc += (f"= {class_name}\n\n")
                    class_adoc += (f"//Include information from owl files\n\n")
                    class_adoc += (f"[#{class_name}]\n")
                    class_adoc += (f"==== {class_name}\n\n")
                    class_adoc += '[plantuml]\n'
                    class_adoc += '....\n'
                    class_adoc += (f"include::../puml/{prefix}_{class_name}.plantuml[] \n")
                    class_adoc += '....\n\n'
                    class_adoc += ('|===\n|Element |Description\n\n')
                    class_adoc += (f"|Type\n|Class\n\n")
                    class_adoc += (f"|Name\n|{class_name}\n\n")
                    class_adoc += (f"|IRI\n|{owl_class}\n\n")

                    #if label != '': class_adoc += (f"|Label\n|{label}\n\n")

                    for superclass_item in superclass:
                        class_adoc += (f"|Subclass of\n|{superclass_item}\n\n")
                    if restrictions != []:
                        for restrictions_item in restrictions:
                            class_adoc += (f"|Restriction\n|{restrictions_item[0]} {restrictions_item[1]} {restrictions_item[2]}\n\n")
                    if disjoints != []:
                        for disjoints_item in disjoints:
                            class_adoc += (f"|Disjoint with\n|{disjoints_item}\n\n")

                    if comments != []:
                        class_adoc += (f"|Comments\n|")
                        for comments_item in comments:
                            if comments_item.startswith("DEF") or comments_item.startswith("USAGE") or comments_item.startswith("EXAMPLE"):
                                class_adoc += (f"{comments_item}\n\n")
                            if comments_item.startswith("HQDM"):
                                term = comments_item.removeprefix("HQDM ")
                                class_adoc += (f"link:http://www.informationjunction.co.uk/hqdm_framework/hqdm_framework/lexical/{term}.htm[Reference to {comments_item}] \n\n")
                    class_adoc += ("|===")

                    fobj.write(class_adoc)

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
                with open(f"{self.__prop_outpath}{prefix}_{property_name}.adoc", 'w', encoding="utf-8") as fobj:

                    prop_adoc=(f"// This file was created automatically by {self.__version}.\n// DO NOT EDIT!\n\n")
                    #prop_adoc += (f"= {property_name}\n\n")
                    prop_adoc += (f"//Include information from owl files\n\n")

                    prop_adoc += (f"[#{property_name}]\n")
                    prop_adoc += (f"==== {property_name}\n\n")
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

                    #if label != '': prop_adoc += (f"|Label\n|{label}\n\n")

                    if comments != []:
                        prop_adoc += (f"|Comments\n|")
                        for comments_item in comments:
                            if comments_item.startswith("DEF") or comments_item.startswith("USAGE") or comments_item.startswith("EXAMPLE"):
                                prop_adoc += (f"{comments_item}\n\n")
                            if comments_item.startswith("HQDM"):
                                term=comments_item.removeprefix("HQDM ")
                                prop_adoc += (f"[Equivalent to {comments_item}] \n\n")

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
                        for restrictions_item in restrictions:
                            if restrictions_item[2] not in card:
                                card.append(restrictions_item[2])
                                plant_uml += fr._get_puml_properties(restrictions_item[2], self.__classes)
                            plant_uml += f'{class_name} ..> {restrictions_item[2]} {random.choice(COLOR)} : {restrictions_item[0]} {restrictions_item[1]}  \n'

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

    def gen_appendix(self):
        appendix_adoc=''
        path=self.__appendix_outpath
        appendix_filename = os.path.join(path, 'Appendix')
        with open(f"{appendix_filename}.adoc", 'w', encoding="utf-8") as fobj:
            appendix_adoc += (f"// This file was created automatically by {self.__version}.\n")
            appendix_adoc += (f"// DO NOT EDIT!\n\n")
            appendix_adoc += (f"= Appendix\n")
            appendix_adoc +=':encoding: utf-8 \n'
            appendix_adoc +=':lang: en \n'
            appendix_adoc +=':table-stripes: even \n'
            appendix_adoc +=':toc: \n'
            appendix_adoc +=':toc-placement!: \n'
            appendix_adoc +=':toclevels: 2 \n'
            appendix_adoc +=':sectnumlevels: 4 \n'
            appendix_adoc +=':sectanchors: \n'
            appendix_adoc +=':figure-id: 0 \n'
            appendix_adoc +=':table-id: 0 \n'
            appendix_adoc +=':req-id: 0 \n'
            appendix_adoc +=':rec-id: 0 \n'
            appendix_adoc +=':per-id: 0 \n'
            appendix_adoc +=':xrefstyle: short \n'
            appendix_adoc +=':chapter-refsig: Clause \n'
            appendix_adoc +=':idprefix: \n'
            appendix_adoc +=':idseparator: \n\n'

            appendix_adoc +='toc::[] \n'
            appendix_adoc +='<<< \n'
            appendix_adoc +='\n'
            appendix_adoc +=':sectnums!: \n\n'
            appendix_adoc += (f"== Core module\n\n")

            appendix_adoc += (f"=== Classes\n\n")
            appendix_adoc +=fr._add_appendix_links(self.__class_outpath, 'Core')
            appendix_adoc +=fr._add_appendix_adoc(self.__class_outpath, 'Core')

            appendix_adoc += (f"=== Properties\n\n")
            appendix_adoc += fr._add_appendix_links(self.__prop_outpath, 'Core')
            appendix_adoc += fr._add_appendix_adoc(self.__prop_outpath, 'Core')

            appendix_adoc += (f"== Domain module\n\n")

            appendix_adoc += (f"=== Classes\n\n")
            appendix_adoc += fr._add_appendix_links(self.__class_outpath, 'Domain')
            appendix_adoc += fr._add_appendix_adoc(self.__class_outpath, 'Domain')

            appendix_adoc += (f"=== Properties\n\n")
            appendix_adoc += fr._add_appendix_links(self.__prop_outpath, 'Domain')
            appendix_adoc += fr._add_appendix_adoc(self.__prop_outpath, 'Domain')

            fobj.write(appendix_adoc)



