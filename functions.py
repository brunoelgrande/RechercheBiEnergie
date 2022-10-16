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
from pyxlsb import open_workbook as open_xlsb
from io import BytesIO

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
        equip_format[x] = prepString(equip_prop[x])[:len(equip_liste[x])]

    # Vérifier avec RegEx pour chacun des 3 équipements si match sur la rangée
    for x in range(len(equip_format)):
        if(re.match(equip_liste[x], equip_format[x])):
            verif[x] = True

    return verif

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


def rechercheRegExPartielle(equip_prop: str, equip_liste: str) -> bool:

    # Initialisation des listes
    verif = False

    # Besoin que l'équipement proposé soit formaté
    equip_prop_format = prepString(equip_prop)
    # Besoin que l'équipement liste soit de la même longueur que l'élément proposé formaté
    equip_liste = equip_liste[:len(equip_prop_format)]

    # Vérifier avec RegEx si match
    if(re.match(equip_liste, equip_prop_format)):
        verif = True

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


@st.cache
def finddMatchePartiels(equip_prop: list[str], df_CEE: pd.DataFrame) -> pd.DataFrame:

    liste_match = []   # [index, match condenseur, match evaporateur, match fournaise]
    df_matchesPart = pd.DataFrame({'': []}) # Empty DF, si tout est faux
    # Faire recherche seulement si au moins 'dim_minimale' caractères :
    dim_minimale = 3
    verif_active = [(len(equip_prop[0]) >= dim_minimale),
                    (len(equip_prop[1]) >= dim_minimale),
                    (len(equip_prop[2]) >= dim_minimale)]

    equip_prop_partiel = ["", "", ""]

    indentation = 0

    # Rechercher tous les appareils encore en vérification (pas encore trouvé de match partiel)
    while verif_active != [False, False, False]:
        indentation += 1

        for x in range(3):

            verif = [False, False, False]

            if verif_active[x]:

                # Ajuster le nombre de lettre à rechercher
                equip_prop_partiel[x] = equip_prop[x][:-indentation]

                if (len(equip_prop_partiel[x]) > dim_minimale):

                    for i in df_CEE.index:
                        equip_liste = [df_CEE['Condenseur_Prep'].iloc[i],
                                       df_CEE['Evaporateur_Prep'].iloc[i],
                                       df_CEE['Fournaise_Prep'].iloc[i]]

                # recherche
                        verif[x] = rechercheRegExPartielle(
                            equip_prop_partiel[x], equip_liste[x])

                        # Si match, on l'ajoute à la liste
                        if (verif[x]):
                            # création d'une liste de listes
                            liste_match.append(
                                [i, verif[0], verif[1], verif[2]])

                        verif = [False, False, False]

                # L'equipement proposé en maintenant trop court, il ne faut plus le vérifier
                else:
                    verif_active[x] = False

        # Est-ce qu'on a trouvé au moins 1 match en enlevement X indentation :
        df_matchesPart = pd.DataFrame(liste_match)

        if (len(df_matchesPart) > 0):
            df_matchesPart.columns = [
                'index', 'Condenseur', 'Evaporateur', 'Fournaise']

            if len(df_matchesPart.query('Condenseur==True')) > 0:
                verif_active[0] = False

            if len(df_matchesPart.query('Evaporateur==True')) > 0:
                verif_active[1] = False

            if len(df_matchesPart.query('Fournaise==True')) > 0:
                verif_active[2] = False

    return df_matchesPart


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


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

@st.cache
def to_excel(df: pd.DataFrame, onglet: str):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name=onglet)
    workbook = writer.book
    worksheet = writer.sheets[onglet]
    format1 = workbook.add_format({'num_format': '0'})
    worksheet.set_column('A:A', None, format1)
    writer.save()
    processed_data = output.getvalue()

    return processed_data


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
