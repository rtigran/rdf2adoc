from helpers import RDF2adoc as r
from helpers import filehelper as f
from datetime import datetime
import sys

config_ok = False

try:
    if len(sys.argv) == 2:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print("This script generates adoc-fragments by parsing an ontology (.ttl) file.\n")
        else:
            config_ok = f.load_config(sys.argv[1])
    else:
        config_ok = f.load_config("./rdf2adoc_config.yml")
    f.logprint("rdf2adoc start at ", datetime.now().strftime("%H:%M:%S"))

except:
    if not config_ok:
        print("Please provide a config.yml file as an argument!")
        print("Call: python rdf2adoc.py <config.yml>")
        sys.exit(-1)

f.prepare_filestructure()

def main():
    ont_inpath = f.get_ont_inpath()
    class_outpath = f.get_adoc_class_outpath()
    reference_class_outpath = f.get_reference_class_outpath()
    prop_outpath = f.get_adoc_prop_outpath()
    reference_prop_outpath = f.get_reference_prop_outpath()
    puml_outpath = f.get_puml_outpath()
    reference_outpath = f.get_reference_outpath()
    diag_gen = f.get_diag_gen()

    rdoc = r(ont_inpath, class_outpath, reference_class_outpath, prop_outpath, reference_prop_outpath, puml_outpath, reference_outpath)
    f.logprint(rdoc.version)
    f.logprint(rdoc.stat)
    rdoc.gen_class_adoc()
    rdoc.gen_prop_adoc()
    rdoc.gen_puml()
    rdoc.gen_reference()

    if diag_gen:
        rdoc.gen_diag()

if __name__ == '__main__':
    main()

f.log_summary()



