from rdflib import Graph
import os


def _add_appendix_adoc(path, prefix):
    appendix_adoc = ''
    if os.path.exists(path):
        for filename in os.listdir(path):
            fullfilename = os.path.join(path, filename)
            if filename.startswith(prefix):
                appendix_adoc += (f"include::.{fullfilename}[]\n\n")
    return appendix_adoc

def _add_appendix_links(path, prefix):
    appendix_adoc = ''
    if os.path.exists(path):
        for filename in os.listdir(path):
            if filename.startswith(prefix):
                filename = filename.split('_')[1].split('.')[0]
                appendix_adoc += (f"link:#{filename}[{filename}] \ \n")
    return appendix_adoc