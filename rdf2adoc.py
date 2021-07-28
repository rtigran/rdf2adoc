from helpers import RDF2adoc as r
from helpers import filehelper as f
import sys

config_ok = False

try:
    config_ok = f.load_config("./rdf2adoc_config.yml")
    f.logprint("rdf2adoc start")
except:
    if not config_ok:
        print("Please provide a config.yml file")
        sys.exit(-1)

f.prepare_filestructure()

ont_inpath=f.get_ont_inpath()
class_outpath=f.get_adoc_class_outpath()
prop_outpath=f.get_adoc_prop_outpath()
diag_outpath=f.get_diag_outpath()

def main(ont_inpath, class_outpath, prop_outpath, diag_outpath):
    rdoc = r(ont_inpath, class_outpath,prop_outpath, diag_outpath)
    f.logprint(rdoc.version)
    f.logprint(rdoc.stat)
    rdoc.gen_class_adoc()
    rdoc.gen_prop_adoc()
    rdoc.gen_diag()

if __name__ == '__main__':
    main(ont_inpath, class_outpath, prop_outpath, diag_outpath)

f.log_summary()



