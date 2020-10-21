import sys
import os
import getopt

import src.log as log
from src.templater import DefaultTemplater
from src.client import DonneesClient
from src.paiement import DonneesPaiement

OUTPUT_FOLDER = "output"
TEMPLATES_FOLDER = "templates"
DOMAINES = ["client", "paiement"]


class Parameters:
    def __init__(self): 
        self.domaine = ""


def read_parameters():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:", ["help", "domaine"])
    except getopt.GetoptError as err:
        log.error(str(err))
        sys.exit(2)

    parameters = Parameters()

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            log.usage()
            sys.exit()
        elif opt in ("-d", "--domaine"):
            parameters.domaine = arg
        else:
            assert False, "Option non prise en compte"

    check_parameters(parameters.domaine)

    return parameters


def check_parameters(domaine):
    # Paramètres obligatoires sinon on sort
    if not domaine:
        log.error("Le domaine du rapport à générer est obligatoire")
        log.usage()
        sys.exit()


def create_output_folder():
     # Création du dossier output s'il n'existe pas
    outputPathFolder = os.path.join(os.getcwd(), OUTPUT_FOLDER)
    if not os.path.exists(outputPathFolder):
        os.mkdir(str(outputPathFolder))


def generate_report(domaine: str):
    template_name = "template_{}.html".format(domaine)
    template_path = os.path.join(os.getcwd(), TEMPLATES_FOLDER, template_name)

    report_name = "rapport_{}.html".format(domaine)
    report_path = os.path.join(os.getcwd(), OUTPUT_FOLDER, report_name)
    
    if domaine not in DOMAINES:
        log.error("Domaine {} inconnu".format(domaine))
    else:
        log.info("Génération du rapport {}...".format(report_name))

        if domaine == "client":
            datas = DonneesClient().tags
        elif domaine == "paiement":
            datas = DonneesPaiement().tags
        
        # Jinja2
        DefaultTemplater(template_path, report_path).render(datas)
        log.info("Rapport {} généré !".format(report_name))


if __name__ == "__main__":
    parameters = read_parameters()
    create_output_folder()
    if parameters.domaine == "all":
        for domaine in DOMAINES:
            generate_report(domaine)
    else:
        generate_report(parameters.domaine)