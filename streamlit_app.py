# -*- coding: utf-8 -*-
"""
Application Streamlit pour faciliter la recherche dans la base de données CEE
Intégration de NEEP à venir

Created on 2022-09-29
@author: Bruno Gauthier
"""
import streamlit as st
import pandas as pd

from functions import *


def main():
    # Settings pour site Streamlit
    st.set_page_config(page_title='Recherche BiEnergie',
                       layout='wide', page_icon=':fire:')

    # Initialisation de variables
    equip_prop = ["", "", ""]

    # Section Hearder de Streamlit

    t1, t2 = st.columns((0.35, 1))

    t1.image('Images/flamme.jpeg', width=380)
    t2.title("Recherche d'appareils pour le programme BiÉnergie")
    t2.header(
        "Évaluation de la compatibilité entres les équipements à air chaud selon la liste CEE")
    t2.subheader(
        "**_Thermopompes - Condenseurs / Évaporateur   |   Fournaise air chaud au gaz naturel_**")

    st.write("---")

    #############

    # Corps du site Streamlit : avec input à gauche et output à droite

    c1, espace, c2 = st.columns((0.25, 0.05, 1))

    c1.subheader("Inscrire les modèles d'appareils recherchés")

    form = c1.form("template_form")

    cond_prop = form.text_input("Condenseur")
    evap_prop = form.text_input("Evaporateur")
    fournaise_prop = form.text_input("Fournaise")

    submit = form.form_submit_button("Rechercher")

    # Une fois le site chargé, charger les données et les préparer

    # Ouverture du fichier excel pour importer la liste complète (critère pour importer Label Energy Star : Yes & Vendu au Canada)
    df_CEE = importData('CEE_data.csv')

    # Préparation des données de la liste CEE pour recherche RegEx
    df_CEE['Condenseur_Prep'] = df_CEE.apply(
        lambda x: prepString(x['Condenseur']), axis=1)

    df_CEE['Evaporateur_Prep'] = df_CEE.apply(
        lambda x: prepString(x['Evaporateur']), axis=1)

    df_CEE['Fournaise_Prep'] = df_CEE.apply(
        lambda x: prepString(x['Fournaise']), axis=1)

    # Au clic du bouton 'Rechercher', trouver les matches et afficher les résultats / suggestions

    if submit:
        equip_prop = [cond_prop.upper(), evap_prop.upper(),
                      fournaise_prop.upper()]

        # Avec fonction de cache pour éviter de reloader les données à chaque fois si les equipements n'ont pas changé.
        df_matches = finddMatches(equip_prop, df_CEE)

        if (len(df_matches) == 0):
            c2.title('Aucun appareil valide')
            c2.error(':warning: Validez votre sélection')

            # Idées  -->  sous routine pour aller chercher des condenseurs avec moins de lettre, pour suggestion ??

        # Si au moins au matches sur un des types d'équipements
        else:

            df_trio = df_CEE.iloc[df_matches.query(
                "Condenseur==True & Evaporateur == True & Fournaise == True")['index']]
            df_duo = df_CEE.iloc[df_matches.query(
                "Condenseur==True & Evaporateur == True")['index']]

            df_cond = df_CEE.iloc[df_matches.query(
                "Condenseur==True")['index']]
            df_evap = df_CEE.iloc[df_matches.query(
                "Evaporateur==True")['index']]

            # Un TRIO existe
            if (len(df_trio) > 0):
                c2.header("Vérification des TRIO  :white_check_mark:")
                # modifier pour un plus beau tableau + éliminer index
                c2.dataframe(df_trio.sort_values('AHRI'),
                             use_container_width=True)
            else:
                c2.header("Vérification des TRIO  :no_entry:")
                c2.write(":warning:  Aucun TRIO n'a été trouvé.")
                c2.write("")

            c2.write("---")

            # Un DUO existe
            if (len(df_duo) > 0):
                c2.header("Vérification des DUO  :white_check_mark:")
                c2.markdown(
                    "**_Vérification de la thermopompe (condenseur et évaporateurs proposés) seulement_**")
                c2.dataframe(df_duo.drop(columns='Fournaise').sort_values(
                    'AHRI'), use_container_width=True)
                c2.write("")

                verif_duo_exp = c2.expander(
                    'Vous avez besion de suggestions de fournaises ?')
                verif_duo_exp.write(phraseAccompagnement(
                    'fournaises', df_duo))  # compléter texte + tableau

                # Ajout tableau des founaises qui pourraient matcher
                fournaise = pd.DataFrame(df_duo['Fournaise'].unique().tolist())
                fournaise.columns = ['Fournaise']
                verif_duo_exp.dataframe(fournaise, use_container_width=True)
                verif_duo_exp.write(
                    '_Attention : bien valider la sélection complète_')

            else:
                c2.header("Vérification des DUO  :no_entry:")
                c2.markdown(
                    "**_Vérification de la thermopompe (condenseur et évaporateurs proposés) seulement_**")
                c2.write(":warning:  Aucun DUO n'a été trouvé.")
                c2.write("")

                # Au moins 1 match sur un condenseur
                if (len(df_matches.query('Condenseur == True')) > 0):
                    verif_duo_exp = c2.expander(
                        "Suggestion d'évaporateurs pour le condenseur sélectionné.")

                    verif_duo_exp.write(
                        phraseAccompagnement('évaporateurs', df_cond))

                    # Ajout tableau des évaporateurs qui pourraient matcher
                    evap = pd.DataFrame(
                        df_cond['Evaporateur'].unique().tolist())
                    evap.columns = ['Évaporateur']
                    verif_duo_exp.dataframe(evap, use_container_width=True)
                    verif_duo_exp.write("")
                    verif_duo_exp.write(
                        '_Attention : bien valider la sélection complète_')

                # Au moins 1 match sur un evaporateur
                if (len(df_matches.query('Evaporateur == True')) > 0):
                    verif_duo_exp = c2.expander(
                        "Suggestion de condenseurs pour l'évaporateur séléectionné.")
                    verif_duo_exp.write(phraseAccompagnement(
                        "condenseurs", df_evap))  # compléter texte + tableau

                    # Ajout tableau des condenseur qui pourraient matcher
                    condenseur = pd.DataFrame(
                        df_evap['Condenseur'].unique().tolist())
                    condenseur.columns = ['Condenseur']
                    verif_duo_exp.dataframe(
                        condenseur, use_container_width=True)
                    verif_duo_exp.write("")
                    verif_duo_exp.write(
                        '_Attention : bien valider la sélection complète_')


if __name__ == "__main__":
    main()
