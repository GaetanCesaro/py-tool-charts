# py-tool-charts
Outil permettant de générer rapidement des graphes d'analyse de données en mode Single Page.
Les graphes sont contenus dans un fichier html unique que l'on peut facilement partager avec d'autres collaborateurs.

Technos utilisées: python, vue.js, jinja2, vuetify, v-charts, pandas 
https://jinja.palletsprojects.com/
https://vuetifyjs.com/fr-FR/introduction/why-vuetify/
https://v-charts.js.org/#/en/README
https://pandas.pydata.org/


## Configuration Workspace

L'outil fonctionne en Python 3.x.

1. Installation Python 3.7 [ici](https://www.python.org/downloads/release/python-374/) ou spérieur 
2. Vérifier que la racine de l'installation Python est bien dans votre PATH (ainsi que le sous dossier Scripts)
3. Lancer les commandes pip ci-dessous à la racine du repo pour récupérer les librairies nécessaires :


```
pip install Jinja2
pip install pandas

```

## Utilisation

### Exemple d'utilisation

```
python rapport.py -d client
-> Génère le rapport correspondant au format HTML dans le dossier output

python rapport.py -d all
-> Génère tous les rapports au format HTML dans le dossier output
```