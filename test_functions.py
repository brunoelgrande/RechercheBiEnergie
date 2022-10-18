# -*- coding: utf-8 -*-
"""
Test pour vérification des fonctions avec pytest
Pour utilisation par : streamlit_app.py

`> pytest` 

Created on 2022-10-17
@author: Bruno Gauthier
"""

from functions import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# Préparation df avec les données

df_CEE = importData('CEE_data.csv')

# Préparation des données de la liste CEE pour recherche RegEx
df_CEE['Condenseur_Prep'] = df_CEE.apply(
    lambda x: prepString(x['Condenseur']), axis=1)

df_CEE['Evaporateur_Prep'] = df_CEE.apply(
    lambda x: prepString(x['Evaporateur']), axis=1)

df_CEE['Fournaise_Prep'] = df_CEE.apply(
    lambda x: prepString(x['Fournaise']), axis=1)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def test_rechercheRegEx():
    assert rechercheRegEx(["123456", "1234", "12345X"], [
                          "1234", "123456", "123456"]) == [True, False, False]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


def test_rechercheRegExPartiellePareil():
    assert rechercheRegExPartielle("12345", "12345") == True


def test_rechercheRegExPartielleCourt1():
    assert rechercheRegExPartielle("123", "12345") == True


def test_rechercheRegExPartielleCourt2():
    assert rechercheRegExPartielle("12345", "123") == True


def test_rechercheRegExPartielleFalse1():
    assert rechercheRegExPartielle("12345", "1234X") == False


def test_rechercheRegExPartielleFalse2():
    assert rechercheRegExPartielle("1234X", "12345") == False


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def test_prepString1():
    assert prepString("(C,H,T)12*+-/") == ".12."


def test_prepString2():
    assert prepString("12345A$%") == "12345A$%"


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# Vérification fonction findMatches()


def test_finddMatcheVide():

    assert finddMatches(["", "", ""], df_CEE).empty


def test_finddMatcheTropCourt():

    assert finddMatches(["YHG", "CM4", "TM9"], df_CEE).empty


def test_finddMatcheManque2():

    assert finddMatches(["YHG42B", "CM48CBC", "TM9Y080C16MP"], df_CEE).empty


def test_finddMatcheSansCondenseur():

    df_test = finddMatches(
        ["", "CM48CBCA1", "TM9Y080C16MP11"], df_CEE)

    df_cond = cleanDF(
        df_CEE, df_test, 'Condenseur')
    df_evap = cleanDF(
        df_CEE, df_test, 'Evaporateur')
    df_fournaise = cleanDF(
        df_CEE, df_test, 'Fournaise')

    resultats = [df_evap.at[0, 'Evaporateur'],
                 df_fournaise.at[0, 'Fournaise']]

    assert resultats == ["CM48CBCA1", "TM9Y080C16MP11"]
    assert df_cond.empty


def test_finddMatcheTropLong():

    df_test = finddMatches(
        ["YHG42B21XXX", "CM48CBCA1XXX", "TM9Y080C16MP11XXX"], df_CEE)

    df_cond = cleanDF(
        df_CEE, df_test, 'Condenseur')
    df_evap = cleanDF(
        df_CEE, df_test, 'Evaporateur')
    df_fournaise = cleanDF(
        df_CEE, df_test, 'Fournaise')

    resultats = [df_cond.at[0, 'Condenseur'],
                 df_evap.at[0, 'Evaporateur'],
                 df_fournaise.at[0, 'Fournaise']]

    assert resultats == ["YHG42B21", "CM48CBCA1", "TM9Y080C16MP11"]
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


# FindMatchePartiels - Liste vide / Court

def test_finddMatchePartielsVide():

    assert finddMatchePartiels(["", "", ""], df_CEE).empty


def test_finddMatchePartielsTropCourt():

    assert finddMatchePartiels(["YHG", "CM4", "TM9"], df_CEE).empty


def test_finddMatchePartielsManque2():

    df_test = finddMatchePartiels(
        ["YHG42B", "CM48CBC", "TM9Y080C16MP"], df_CEE)

    df_condPartiel = cleanDF(
        df_CEE, df_test, 'Condenseur')
    df_evapPartiel = cleanDF(
        df_CEE, df_test, 'Evaporateur')
    df_fournaisePartiel = cleanDF(
        df_CEE, df_test, 'Fournaise')

    resultats = [df_condPartiel.at[0, 'Condenseur'],
                 df_evapPartiel.at[0, 'Evaporateur'],
                 df_fournaisePartiel.at[0, 'Fournaise']]

    assert resultats == ["YHG42B21", "CM48CBBA1", "TM9Y080C16MP11"]


def test_finddMatchePartielsSansCondenseur():

    df_test = finddMatchePartiels(
        ["", "CM48CBC", "TM9Y080C16MP"], df_CEE)

    df_condPartiel = cleanDF(
        df_CEE, df_test, 'Condenseur')
    df_evapPartiel = cleanDF(
        df_CEE, df_test, 'Evaporateur')
    df_fournaisePartiel = cleanDF(
        df_CEE, df_test, 'Fournaise')

    resultats = [df_evapPartiel.at[0, 'Evaporateur'],
                 df_fournaisePartiel.at[0, 'Fournaise']]

    assert resultats == ["CM48CBBA1", "TM9Y080C16MP11"]
    assert df_condPartiel.empty


def test_finddMatchePartielsTropLong():

    df_test = finddMatchePartiels(
        ["YHG42B21XXX", "CM48CBCA1XXX", "TM9Y080C16MP11XXX"], df_CEE)

    df_condPartiel = cleanDF(
        df_CEE, df_test, 'Condenseur')
    df_evapPartiel = cleanDF(
        df_CEE, df_test, 'Evaporateur')
    df_fournaisePartiel = cleanDF(
        df_CEE, df_test, 'Fournaise')

    resultats = [df_condPartiel.at[0, 'Condenseur'],
                 df_evapPartiel.at[0, 'Evaporateur'],
                 df_fournaisePartiel.at[0, 'Fournaise']]

    assert resultats == ["YHG42B21", "CM48CBCA1", "TM9Y080C16MP11"]
