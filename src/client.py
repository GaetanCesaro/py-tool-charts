from datetime import datetime
import datetime as dt
import pandas as pd
import psycopg2
import math

import src.config as c


def truncate(number, decimals=0):
        """
        Returns a value truncated to a specific number of decimal places.
        """
        if not isinstance(decimals, int):
            raise TypeError("decimal places must be an integer.")
        elif decimals < 0:
            raise ValueError("decimal places has to be 0 or more.")
        elif decimals == 0:
            return math.trunc(number)

        factor = 10.0 ** decimals
        return math.trunc(number * factor) / factor


class DonneesClient:

    tags={}

    def __init__(self):
        ###########################################################################
        # Connexion BDD
        cxPG = psycopg2.connect(c.ENVIRONNEMENTS["PRD"]["servers"]["POSTGRE"])
    
        # Requêtage de la BDD
        dif_notification = pd.read_sql("select * from sgendif.dif_notification where date_creation > NOW() - interval '365 day'", cxPG)
        cli_personne_physique = pd.read_sql("select * from sgencli.cli_personne_physique where date_modification > NOW() - interval '365 day'", cxPG)
        gpp_moyen_contact_view = pd.read_sql("select * from sgengpp.moyen_contact_view where date_debut_validite > NOW() - interval '365 day' or date_fin_validite > NOW() - interval '365 day'", cxPG)

        # Fermeture de la connexion BDD
        cxPG = None
        ###########################################################################

        ###########################################################################
        # Notification Diffusées / Non éligibles
        nbNotificationsDiffusees=0
        nbNotificationsNonEligibles=0
        nbNotificationsTotal=0
        pourcentageNotificationsDiffusees=0.0
        pourcentageNotificationsNonEligibles=0.0
        rowsNotificationsDaily=[]

        for k, g in dif_notification.groupby([dif_notification['date_creation'].dt.date]):
            nbNotificationsDiffusees+=len(g[g.statut=='DIFFUSE'])
            nbNotificationsNonEligibles+=len(g[g.statut=='NON_ELIGIBLE'])

            data = {
                'Diffusee': len(g[g.statut=='DIFFUSE']), 
                'Non eligible': len(g[g.statut=='NON_ELIGIBLE']), 
                'Date': str(k)
            }
            rowsNotificationsDaily.append(data)

        nbNotificationsTotal=nbNotificationsDiffusees+nbNotificationsNonEligibles
        pourcentageNotificationsDiffusees=truncate(nbNotificationsDiffusees/nbNotificationsTotal*100, 2)
        pourcentageNotificationsNonEligibles=100-pourcentageNotificationsDiffusees
        colsNotificationsDaily=list(rowsNotificationsDaily[0].keys())
        metricsNotificationsDaily=['Diffusee', 'Non eligible']
        dimNotificationsDaily=['Date']

        ###########################################################################
        # Notifications par Type
        rowsNotificationsType=[]
        for k, g in dif_notification.groupby(['type']):
            rowsNotificationsType.append({
                'Notification': len(g),
                'Type': str(k)})
        colsNotificationsType=list(rowsNotificationsType[0].keys())
        metricsNotificationsType=['Notification']
        dimNotificationsType=['Type']

        ###########################################################################
        # Comptes activés/créés/désactivés
        nbComptesActives=0
        nbComptesCrees=0
        nbComptesDesactives=0
        rowsComptesDaily=[]

        for k, g in cli_personne_physique.groupby([cli_personne_physique['date_modification'].dt.date]):
            nbComptesActives+=len(g[g.statut_compte_assure=='ACTIVE'])
            nbComptesCrees+=len(g[g.statut_compte_assure=='CREE'])
            nbComptesDesactives+=len(g[g.statut_compte_assure=='DESACTIVE'])

            # Après la RDD de la colonne statut_compte_assure sinon ça biaise le graphique
            if str(k) > '2020-02-25':
                data = {
                    'ACTIVE': len(g[g.statut_compte_assure=='ACTIVE']), 
                    'CREE': len(g[g.statut_compte_assure=='CREE']), 
                    'DESACTIVE': len(g[g.statut_compte_assure=='DESACTIVE']), 
                    'Date': str(k)
                }
                rowsComptesDaily.append(data)

        colsComptesDaily=list(rowsComptesDaily[0].keys())
        metricsComptesDaily=['ACTIVE', 'CREE', 'DESACTIVE']
        dimComptesDaily=['Date']

        ###########################################################################
        # Moyens de contacts mis à jour chaque jour depuis l'Espace Client
        nbAdressesModifiees=0
        nbTelephonesModifies=0
        nbEmailsModifies=0
        rowsMajContactDaily=[]

        for k, g in gpp_moyen_contact_view[gpp_moyen_contact_view.origine=='SOA'].groupby([gpp_moyen_contact_view['date_fin_validite'].dt.date]):
            nbAdressesModifiees += len(g[g.adresse_domicile.notnull()]) + len(g[g.boite_postale.notnull()])
            nbTelephonesModifies += len(g[g.telephone_fixe.notnull()]) + len(g[g.telephone_mobile.notnull()])
            nbEmailsModifies += len(g[g.email.notnull()])

            # Exclusion des dates où des correction d'adresse en masse ont été faites
            if str(k) not in ('2020-01-16', '2020-02-24', '2020-02-26', '2020-03-03', '2020-03-04', '2020-06-11', '2020-06-23'):
                data = {
                    'ADRESSE': len(g[g.adresse_domicile.notnull()]) + len(g[g.boite_postale.notnull()]), 
                    'TELEPHONE': len(g[g.telephone_fixe.notnull()]) + len(g[g.telephone_mobile.notnull()]), 
                    'EMAIL': len(g[g.email.notnull()]), 
                    'Date': str(k)
                }
                rowsMajContactDaily.append(data)

        colsMajContactDaily=list(rowsMajContactDaily[0].keys())
        metricsMajContactDaily=['ADRESSE', 'TELEPHONE', 'EMAIL']
        dimMajContactDaily=['Date']

        ###########################################################################
        # Stockage des données
        self.tags = {
            'date': "'" + datetime.now().strftime("%d/%m/%Y %Hh%M") + "'",
            'nbComptesActives': str(nbComptesActives),
            'nbComptesCrees': str(nbComptesCrees),
            'nbComptesDesactives': str(nbComptesDesactives),
            'rowsComptesDaily': rowsComptesDaily,
            'colsComptesDaily': colsComptesDaily,
            'metricsComptesDaily': metricsComptesDaily,
            'dimComptesDaily': dimComptesDaily,
            'nbAdressesModifiees': str(nbAdressesModifiees),
            'nbTelephonesModifies': str(nbTelephonesModifies),
            'nbEmailsModifies': str(nbEmailsModifies),
            'rowsMajContactDaily': rowsMajContactDaily,
            'colsMajContactDaily': colsMajContactDaily,
            'metricsMajContactDaily': metricsMajContactDaily,
            'dimMajContactDaily': dimMajContactDaily,
            'nbNotificationsDiffusees': str(nbNotificationsDiffusees),
            'nbNotificationsNonEligibles': str(nbNotificationsNonEligibles),
            'pourcentageNotificationsDiffusees': str(pourcentageNotificationsDiffusees),
            'pourcentageNotificationsNonEligibles': str(pourcentageNotificationsNonEligibles),
            'rowsNotificationsDaily': rowsNotificationsDaily,
            'colsNotificationsDaily': colsNotificationsDaily,
            'metricsNotificationsDaily': metricsNotificationsDaily,
            'dimNotificationsDaily': dimNotificationsDaily,
            'rowsNotificationsType': rowsNotificationsType,
            'colsNotificationsType': colsNotificationsType,
            'metricsNotificationsType': metricsNotificationsType,
            'dimNotificationsType': dimNotificationsType,
        }
