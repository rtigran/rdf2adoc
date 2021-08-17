from datetime import datetime
import os
from os import listdir
from os.path import isfile, join

import yaml

dic_config = {}

errorcount = 0

def load_config(configfile : str) -> bool:
    if os.path.exists(configfile):
        with open(configfile, 'r', encoding="utf-8") as fobj:
            global dic_config
            dic_config = yaml.safe_load(fobj).copy()
            return True
    else:
        print("Config file not found!")
        return False


def get_ont_inpath() ->str:
    path=dic_config["ont_inpath"]
    ont_files=[f for f in listdir(path) if isfile(join(path,f))]
    return join(path,ont_files[0])

def get_adoc_class_outpath() -> str:
    return dic_config["adoc_class_outpath"] if "adoc_class_outpath" in dic_config else ""

def get_adoc_prop_outpath() -> str:
    return dic_config["adoc_prop_outpath"] if "adoc_class_outpath" in dic_config else ""

def get_puml_outpath() ->str:
    return os.path.abspath(dic_config["puml_outpath"]) if "puml_outpath" in dic_config else ""

def get_diag_gen() -> str:
    return dic_config["diag_gen"] if "diag_gen" in dic_config else "False"

def get_diag_outpath() -> str:
    return os.path.abspath(dic_config["diag_outpath"]) if "diag_outpath" in dic_config else ""

def get_plantuml_jar() -> str:
    return os.path.abspath(dic_config["plantuml_jar"]) if "plantuml_jar" in dic_config else ""

def prepare_filestructure() -> None:
    if os.path.exists(dic_config["logfile"]):
        os.remove(dic_config["logfile"])
    if get_adoc_class_outpath():
        clean_filestructure(get_adoc_class_outpath())
    if get_adoc_prop_outpath():
        clean_filestructure(get_adoc_prop_outpath())
    if get_puml_outpath():
        clean_filestructure(get_puml_outpath())
    if get_diag_outpath():
        clean_filestructure(get_diag_outpath())

def clean_filestructure(path : str) -> None:
    if os.path.exists(path):
        for filename in os.listdir(path):
            fullfilename = os.path.join(path, filename)
            if os.path.isfile(fullfilename):
                os.remove(fullfilename)
    else:
        os.makedirs(path)

def logprint(message : str, end=" ") -> None:
    try:
        if dic_config["logging"]:
            print(message, end)

            with open(dic_config["logfile"], 'a') as fobj:
                print(message, end, file=fobj)
    except:
        # user configured no logging mode
        pass


def log_error( message : str, file : str = "", line : int = -1,) -> None:
    if line > -1:
        logprint(f"Error: {message} in line {line} of {file}!")
    elif file:
        logprint(f"Error: {message} in {file}")
    else:
        logprint(f"Error: {message}")
    global errorcount
    errorcount += 1


def log_summary() -> None :
    if (errorcount):
        logprint(f"rdf2adoc finished with {errorcount} WARNINGS")
    else:
        logprint("rdf2adoc finished OK at ", datetime.now().strftime("%H:%M:%S"))