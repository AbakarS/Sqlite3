
# les codes de base pour connecter une base de donnée SQL à python
import pandas as pd
import sqlite3
import math

# Créer une connexion à la base de données
connexion=sqlite3.connect("factbook.db")

#lire la table 'facts' avec pandas sous forme d'un DataFrame
a=pd.read_sql_query("select * from facts;", con=connexion)

#Afficher la table 
#print(a)

#------------------------------------------------------------------------------
"""
L'idée c'est d'avoir une estimation de la population en 2050 pour chaque pays. Actuellement, nous avons une base de données avec le nombre 
d'habitants en 2015 et nous avons un taux de croissance.

population : colonne de la population initiale de janvier 2015
population_growth : la colonne de la croissance annuelle de la population. Si on suppose cette croissance est constante jusqu'à 2050, alors
nous sommes sûrs d'avoir une estimation fiable du nombre d'habitants en 2050.

On utilisera la formule mathématique ci-dessous pour calculer cette estimation

"""



#le nombre de 10 pays le plus peuplés en 2050
#N=N0*e(rt)

#N : population finale, la population de 2050
#N0 : c'est la population initiale, la population de 15
#e : c'est une constante qu'on obtient dans la librairie 'math'
#r : c'est le taux de croissance annuelle exprimé en décimal
#t : nombre d'années entre l'estimation et l'initiale

# Exemple : 5000 habitants, taux de croissance t de 4% 2015 ---> 2050, donc t = 35 ans

# 5000*e**(0.04*35)

#------------------------------------------------------------------------------------------
#Nous transmettons l'exemple de la fonction mathématique ci-dessous dans une fonction python

def pop_groupe(x):
	return x['population']*math.e**((x['population_growth']/100)*35)

# On utilise la méthode 'apply' pour appliquer la fonction 'pop-gorupe()' à notre table 'facts' 
# Nous créeons en même temps la colonne 'pop_2050'

a['pop_2050']=a.apply(lambda row:pop_groupe(row), axis =1)

#Supprimer les valeurs manquantes (na)
a=a.dropna(axis=0)

# On va filtrer les pays qui ont une surface terrestre égale à zero (0) ou manquante 
# on filtrera aussi les pays qui ont une population égale à zero (0) ou manquante

a=a[(a['area_land']>0) & (a['population'] > 0)]

#Afficher les noms de 10 pays le plus peuplé en 2050

b = a.sort_values(['pop_2050'], ascending=[False])

b=b['name'].iloc[0:9]

#Afficher la variable b
print("Afficher les noms de 10 pays le plus peuplé en 2050 :" , "\n", b)

#Insertion d'espace
# Calculer le ratio de la surface terrestre totale sur la surface
# des océans totale appartenant aux pays de la table facts

df=pd.read_sql_query("select sum(area_land), sum(area_water) from facts where area_land!=''", con=connexion)

# On affiche dans un tableau pandas les sommes des surfaces terrestres et surfaces de l'eau pour chaque pays

print(df)

#Insertion d'espace
print()

#On affiche le ratio Terre / Mer
print("On affiche le ratio Terre / Mer :", "\n", df['sum(area_land)']/df['sum(area_water)'])

#On a 28% plus de terre que de mer. 

