import os
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

    return dic_config["ont_inpath"] if "ont_inpath" in dic_config else ""

def get_adoc_class_outpath() -> str:
    return dic_config["adoc_class_outpath"] if "adoc_class_outpath" in dic_config else ""

def get_adoc_prop_outpath() -> str:
    return dic_config["adoc_prop_outpath"] if "adoc_class_outpath" in dic_config else ""


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
        logprint(f"Rdfdoc finished with {errorcount} WARNINGS")
    else:
        logprint("Rdfdoc finished OK")