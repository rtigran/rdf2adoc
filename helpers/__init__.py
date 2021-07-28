from rdflib import Graph
import subprocess
from helpers import class_parser as cp
from helpers import property_parser as pp
from helpers import ont_version as v
from helpers import filehelper as f

class RDF2adoc:
    def __init__(self, filepath : str, class_outpath : str, prop_outpath : str, diag_outpath : str, format='turtle'):
        self.__filepath = filepath
        self.__class_outpath = class_outpath
        self.__prop_outpath = prop_outpath
        self.__diag_outpath=diag_outpath

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
            self.__classes.sort()
            for class_uri, prefix, class_name, label, comment, superclass, restrictions, disjoints in self.__classes:
                with open(f"{self.__class_outpath}{class_name}.adoc", 'w', encoding="utf-8") as fobj:

                    fobj.write(f"// This file was created automatically by {self.__version}.\n// DO NOT EDIT!\n\n")
                    fobj.write(f"= {class_name}\n\n")
                    fobj.write(f"//Include information from owl files\n\n")
                    fobj.write(f"The following model provides an overview of {prefix}:{class_name}\n\n")
                    fobj.write('|===\n|Element |Description\n\n')
                    fobj.write(f"|Type\n|owl:Class\n\n")
                    fobj.write(f"|Name\n|{class_name}\n\n")
                    fobj.write(f"|IRI\n|{class_uri}\n\n")

                    if label != '': fobj.write(f"|Label\n|{label}\n\n")

                    for superclass_item in superclass:
                        fobj.write(f"|Subclass of\n|{superclass_item}\n\n")
                    if restrictions != []:
                        for restrictions_item in restrictions:
                            fobj.write(f"|Restriction\n|{restrictions_item}\n\n")
                    if disjoints != []:
                        for disjoints_item in disjoints:
                            fobj.write(f"|Disjoint with\n|{disjoints_item}\n\n")

                    if comment != '': fobj.write(f"|Comment\n|{comment}\n\n")
                    fobj.write("|===")

    def gen_prop_adoc(self):
        if self.__properties:
            self.__properties.sort()
            for property_uri, prefix, property_name, label, comment, subPropertyOf, domain, range1, inverse_of, characteristics in self.__properties:
                with open(f"{self.__prop_outpath}{property_name}.adoc", 'w', encoding="utf-8") as fobj:

                    fobj.write(f"// This file was created automatically by {self.__version}.\n// DO NOT EDIT!\n\n")
                    fobj.write(f"= {property_name}\n\n")
                    fobj.write(f"//Include information from owl files\n\n")
                    fobj.write(f"The following model provides an overview of {prefix}:{property_name}\n\n")
                    fobj.write('|===\n|Element |Description\n\n')
                    fobj.write(f"|Type\n|owl:ObjectProperty\n\n")
                    fobj.write(f"|Name\n|{property_name}\n\n")
                    fobj.write(f"|IRI\n|{property_uri}\n\n")
                    if subPropertyOf != []:
                        for subPropertyOf_item in subPropertyOf:
                            fobj.write(f"|Subproperty of\n|{subPropertyOf_item}\n\n")

                    if domain != []:
                        for domain_item in domain:
                            fobj.write(f"|Has domain\n|{domain_item}\n\n")
                    if range1 != []:
                        for range1_item in domain:
                            fobj.write(f"|Has range\n|{range1_item}\n\n")
                    if inverse_of != []:
                        for inverse_of_item in inverse_of:
                            fobj.write(f"|Inverse\n|{inverse_of_item}\n\n")
                    if characteristics != []:
                        for characteristics_item in characteristics:
                            fobj.write(f"|Characteristic\n|{characteristics_item}\n\n")

                    if label != '': fobj.write(f"|Label\n|{label}\n\n")
                    if comment != '': fobj.write(f"|Comment\n|{comment}\n\n")

                    fobj.write("|===")

    def gen_diag(self):
        try:
            if f.get_plantuml_jar():
                f.logprint("plantuml starting...")
                print(f.get_plantuml_jar(), f.get_puml_inpath(), f.get_diag_outpath())
                #subprocess.run(["java", "-jar", f.get_plantuml_jar(), f.get_puml_inpath(), "-o", f.get_diag_outpath()])

                f.logprint("plantuml finished")
        except:
            f.logprint("no plantuml.jar defined or found")

