# -*- coding: utf-8 -*-
"""
Ensemble des fonctions utilisées pour la recheche BiÉnergie
Pour utilisation par : rechercherBiEnergie.py

Created on 2022-09-29
@author: Bruno Gauthier
"""

import streamlit as st
import re
import pandas as pd


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


def prepString(String: str) -> str:
    # Remplace les parenthèses de type Wildcard par '.' pour RegEx
    while(String.find('(') != -1):
        String = String[:String.index('(')]+'.' + String[String.index(')')+1:]

    # Éliminie les caractères spéciaux par "" et '*' par '.' pour WildCard RegEx
    return String.replace('+', '').replace('-', '').replace('/', '').replace('*', '.')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


def importData(nom_fichier: str) -> pd.DataFrame:

    df = pd.read_csv(nom_fichier, index_col='index')

    return df
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


def rechercheRegEx(equip_prop: list[str], equip_liste: list[str]) -> list[bool]:

    # Initialisation des listes
    equip_format = ["", "", ""]
    verif = [False, False, False]

    # Besoin que l'équipement proposé soit de la même longueur que l'élément vérifié de la liste
    for x in range(len(equip_prop)):
        equip_format[x] = prepString(equip_prop[x])
        equip_format[x] = equip_format[x][:len(equip_liste[x])]

    # Vérifier avec RegEx pour chacun des 3 équipements si match sur la rangée
    for x in range(len(equip_format)):
        if(re.match(equip_liste[x], equip_format[x])):
            verif[x] = True

    return verif

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


@st.cache
def finddMatches(equip_prop: list[str], df_CEE: pd.DataFrame) -> pd.DataFrame:

    liste_match = []   # [Index de liste, match condenseur, match evaporateur, match fournaise]

    for i in df_CEE.index:
        equip_liste = [df_CEE['Condenseur_Prep'].iloc[i],
                       df_CEE['Evaporateur_Prep'].iloc[i],
                       df_CEE['Fournaise_Prep'].iloc[i]]

        verif = rechercheRegEx(equip_prop, equip_liste)

        # Si au moins 1 match, on l'ajoute à la liste
        if (verif[0] | verif[1] | verif[2]):
            # création d'une liste de listes
            liste_match.append([i, verif[0], verif[1], verif[2]])

    # Création d'un df avec tous les matches
    df_matches = pd.DataFrame(liste_match)
    if (len(df_matches) > 0):
        df_matches.columns = [
            'index', 'Condenseur', 'Evaporateur', 'Fournaise']

    return df_matches

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


def phraseAccompagnement(type_equip: str, df: pd.DataFrame) -> str:

    texte = ""

    listeMarque = df['Marque'].unique().tolist()

    # S'il y a seulement 1 marque
    if (len(listeMarque) == 1):
        texte += f"Des {type_equip} de la marque {listeMarque[0]} pourraient accompagner la sélection."

    # S'il y a plusieurs marques
    else:
        texte += f"Des {type_equip} de marques "

        for i in range(len(listeMarque)):
            texte += listeMarque[i]

            if i < (len(listeMarque)-2):
                texte += ", "

            if i == (len(listeMarque)-2):
                texte += " et "

            if i == (len(listeMarque)-1):
                texte += " pourraient accompagner la sélection."

    return texte
