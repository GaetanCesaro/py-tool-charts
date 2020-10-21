from datetime import datetime
import datetime as dt
import pandas as pd
import psycopg2
import src.log as log
import src.config as c

class DonneesPaiement:

    tags={}

    def __init__(self):
        ###########################################################################
        # Connexion BDD
        cxPG = psycopg2.connect(c.ENVIRONNEMENTS["PRD"]["servers"]["POSTGRE"])

        # Reading part
        rs = pd.read_sql("select date(date_creation) as date_paiement, sum(montant) as montant_global, count(*) as nombre_paiement " +
        "from srecreg.reg_reglement " +
        "where mode_paiement = 'CB_EN_LIGNE' and statut IN ('VALIDE', 'EN_TRAITEMENT', 'CONFIRME') " +
        "group by date(date_creation);", cxPG)
        
        # Fermeture de la connexion BDD
        cxPG = None
        ###########################################################################

        ###########################################################################
        # Building Charts datas
        nbTotReglement=0
        rows1=[]
        for k, g in rs.groupby(['date_paiement']):
            nbTotReglement+=g.nombre_paiement.iloc[0]
            rows1.append({
                'Nombre de reglements': str(g.nombre_paiement.iloc[0]), 
                'Date': str(k)})
        cols1=list(rows1[0].keys())
        metrics1=["Nombre de reglements"]
        dim1=["Date"]

        mtTotReglement=0
        rows2=[]
        for k, g in rs.groupby(['date_paiement']):
            mtTotReglement+=g.montant_global.iloc[0]
            rows2.append({
                'Montant des reglements': str(g.montant_global.iloc[0]), 
                'Date': str(k)})
        cols2=list(rows2[0].keys())
        metrics2=["Montant des reglements"]
        dim2=["Date"]


        self.tags = {
            'date': "'" + datetime.now().strftime("%d/%m/%Y %Hh%M") + "'",
            'nbTotReglement': str(nbTotReglement),
            'mtTotReglement': str(mtTotReglement),
            'rows1': rows1,
            'cols1': cols1,
            'metrics1': metrics1,
            'dim1': dim1,
            'rows2': rows2,
            'cols2': cols2,
            'metrics2': metrics2,
            'dim2': dim2,
        }
