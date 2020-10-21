# -*- coding: utf-8 -*-
ENVIRONNEMENTS = {
    "DEV": {
        "schema_name": "DEV",
        "servers": {
            "DB2": "DRIVER={iSeries Access ODBC Driver};SYSTEM=system;SERVER=server;DATABASE=database;UID=user;PWD=password",
            "POSTGRE": "host=hostname port=1234 user=user password=password dbname=dbname"
        }
    },
}