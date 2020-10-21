# -*- coding: utf-8 -*-
from tqdm import tqdm
from termcolor import colored

LOGLEVEL = "INFO"

# Logs tqdm configuration
def debug(msg): 
    if LOGLEVEL == "DEBUG":
        tqdm.write(colored('[DEBUG] ' + msg, 'yellow'))

def info(msg): tqdm.write(colored('[INFO] ' + msg, 'green'))
def warn(msg): tqdm.write(colored('[WARN] ' + msg, 'magenta'))
def error(msg): tqdm.write(colored('[ERROR] --> ' + msg, 'red'))

# Usage
def usage():
    warn("Utilisation : ")
    warn("python rapport.py -d <domaine>")
    warn("")
    warn("Options : ")
    warn("-d <domaine> (--domaine) : Domaine du rapport que l'on souhaite générer")
    warn("---")
    warn("  Domaines possibles : client, all(tous les domaines)")
    warn("  Exemples: py rapport.py -d client")
    warn("            py rapport.py -d all")
    warn("---")