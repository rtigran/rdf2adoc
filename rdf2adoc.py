from helpers import Rdfdoc as r
from helpers import filehelper as f
import sys

config_ok = False

try:
    config_ok = f.load_config("./rdf2adoc_config.yml")
    f.logprint("Rdfdoc start")
except:
    if not config_ok:
        print("Please provide a config.yml file")
        sys.exit(-1)

ont_inpath=f.get_ont_inpath()
class_outpath=f.get_adoc_class_outpath()
prop_outpath=f.get_adoc_prop_outpath()

def main(ont_inpath, class_outpath, prop_outpath):
    rdoc = r(ont_inpath, class_outpath,prop_outpath)
    f.logprint(rdoc.version)
    f.logprint(rdoc.stat)
    rdoc.gen_class_adoc()
    rdoc.gen_prop_adoc()

if __name__ == '__main__':
    main(ont_inpath, class_outpath, prop_outpath)

f.log_summary()



