# -*- coding: utf-8 -*-
"""
Application Streamlit pour faciliter la recherche dans la base de données CEE
Intégration de NEEP à venir

Created on 2022-09-29
@author: Bruno Gauthier
"""
import streamlit as st
import pandas as pd
from pyxlsb import open_workbook as open_xlsb
from io import BytesIO
from datetime import datetime

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

    c1.subheader("Recherche par modèles d'appareils")

    form = c1.form("template_form")

    cond_prop = form.text_input("Condenseur")
    evap_prop = form.text_input("Evaporateur")
    fournaise_prop = form.text_input("Fournaise")

    submit_Appareils = form.form_submit_button("Rechercher")

    # Recherche par numéro AHRI
    c1.subheader("Recherche par numéro AHRI")

    formAHRI = c1.form("template_form_AHRI")

    num_AHRI = formAHRI.text_input("Numéro AHRI")

    submit_AHRI = formAHRI.form_submit_button("Rechercher")

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

    if submit_Appareils:
        equip_prop = [cond_prop.upper(), evap_prop.upper(),
                      fournaise_prop.upper()]

        # Avec fonction de cache pour éviter de reloader les données à chaque fois si les equipements n'ont pas changé.
        df_matches = finddMatches(equip_prop, df_CEE)

        if df_matches.empty:
            c2.title('Aucun appareil valide :no_entry:')
            c2.error(':warning: Validez votre sélection')

        # Préparation de propositions si aucun match :

            with st.spinner(":hourglass: Recherche en cours"):

                df_matchesPartiels = finddMatchePartiels(
                    equip_prop, df_CEE)

                if not df_matchesPartiels.empty:

                    df_condPartiel = cleanDF(
                        df_CEE, df_matchesPartiels, 'Condenseur')
                    df_evapPartiel = cleanDF(
                        df_CEE, df_matchesPartiels, 'Evaporateur')
                    df_fournaisePartiel = cleanDF(
                        df_CEE, df_matchesPartiels, 'Fournaise')

                    if not df_matchesPartiels.empty:
                        c2.info(
                            "Proposition d'appreils près de vos sélections")
                    if not df_condPartiel.empty:
                        c2.write(
                            'Liste de condenseurs près de votre sélection')
                        c2.dataframe(df_condPartiel,
                                     use_container_width=True)
                    if not df_evapPartiel.empty:
                        c2.write(
                            "Liste d'évaporateurs près de votre sélection")
                        c2.dataframe(df_evapPartiel,
                                     use_container_width=True)
                    if not df_fournaisePartiel.empty:
                        c2.write(
                            'Liste de fournaises près près de votre sélection')
                        c2.dataframe(df_fournaisePartiel,
                                     use_container_width=True)

        # Si au moins au matches sur un des types d'équipements
        else:

            df_trio = (df_CEE
                       .iloc[df_matches.query("Condenseur==True & Evaporateur == True & Fournaise == True")['index']]
                       .drop(['Condenseur_Prep', 'Evaporateur_Prep', 'Fournaise_Prep'], axis=1)
                       .reset_index(drop=True)
                       .sort_values('AHRI'))

            df_duo = (df_CEE
                      .iloc[df_matches.query("Condenseur==True & Evaporateur == True")['index']]
                      .drop(['Condenseur_Prep', 'Evaporateur_Prep', 'Fournaise_Prep'], axis=1)
                      .reset_index(drop=True)
                      .sort_values('AHRI'))

            df_cond = (df_CEE
                       .iloc[df_matches.query("Condenseur==True")['index']]
                       .drop(['Condenseur_Prep', 'Evaporateur_Prep', 'Fournaise_Prep'], axis=1)
                       .reset_index(drop=True))
            df_evap = (df_CEE
                       .iloc[df_matches.query("Evaporateur==True")['index']]
                       .drop(['Condenseur_Prep', 'Evaporateur_Prep', 'Fournaise_Prep'], axis=1)
                       .reset_index(drop=True))

            df_fournaise = (df_CEE
                            .iloc[df_matches.query("Fournaise==True")['index']]
                            .drop(['Condenseur_Prep', 'Evaporateur_Prep', 'Fournaise_Prep'], axis=1)
                            .reset_index(drop=True))

            # Un TRIO existe
            if not df_trio.empty:
                c2.header("Vérification des TRIO  :white_check_mark:")
                # modifier pour un plus beau tableau + éliminer index
                c2.dataframe(df_trio,
                             use_container_width=True)

                # Bouton Download TRIO
                df_temp = (df_trio
                           .sort_values('AHRI')
                           .reset_index(drop=True)
                           )
                df_temp.at[0, 'Condenseur Proposé'] = equip_prop[0]
                df_temp.at[0, 'Évaporateur Proposé'] = equip_prop[1]
                df_temp.at[0, 'Vérifié le'] = datetime.now()
                c2.download_button(
                    label="📥 Télécharger résultats TRIO",
                    data=to_excel(df_temp, 'Trio'),
                    file_name='resultat_trio.xlsx')

            else:
                c2.header("Vérification des TRIO  :no_entry:")
                c2.write(":warning:  Aucun TRIO n'a été trouvé.")
                c2.write("")

            c2.write("---")

            # Un DUO existe
            if not df_duo.empty:
                c2.header("Vérification des DUO  :white_check_mark:")
                c2.markdown(
                    "**_Vérification de la thermopompe (condenseur et évaporateurs proposés) seulement_**")
                c2.dataframe(df_duo.drop(columns='Fournaise').reset_index(
                    drop=True), use_container_width=True)

                # Bouton Download DUO
                df_temp = (df_duo
                           .drop(columns='Fournaise')
                           .reset_index(drop=True)
                           )
                df_temp.at[0, 'Condenseur Proposé'] = equip_prop[0]
                df_temp.at[0, 'Évaporateur Proposé'] = equip_prop[1]
                df_temp.at[0, 'Vérifié le'] = datetime.now()

                c2.download_button(
                    label="📥 Télécharger résultats DUO",
                    data=to_excel(df_temp, 'Duo'),
                    file_name='resultat_duo.xlsx')

                c2.write("")

                verif_duo_exp = c2.expander(
                    'Vous avez besion de suggestions de fournaises ?')
                verif_duo_exp.write(phraseAccompagnement(
                    'fournaises', df_duo))  # compléter texte + tableau

                sugg_fournaise = (df_duo
                                  .filter(['Marque', 'Fournaise'])
                                  .drop_duplicates()
                                  .sort_values(['Marque', 'Fournaise'])
                                  .reset_index(drop=True))

                verif_duo_exp.dataframe(sugg_fournaise.filter(
                    ['Fournaise']), use_container_width=True)

                sugg_fournaise.at[0, 'Condenseur Proposé'] = equip_prop[0]
                sugg_fournaise.at[0, 'Évaporateur Proposé'] = equip_prop[1]
                sugg_fournaise.at[0, 'Vérifié le'] = datetime.now()

                # Bouton Download FOURNAISES proposées
                verif_duo_exp.download_button(
                    label="📥 Télécharger propositions FOURNAISES",
                    data=to_excel(sugg_fournaise,
                                  'Propositions FOURNAISES'),
                    file_name='propositions_fournaises.xlsx')

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

                    c2.success("Le condenseur est un modèle admissible.")

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

                    c2.success("L'évaporateur est un modèle admissible.")

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

                # Au moins 1 match sur une fournaise
                if (len(df_matches.query('Fournaise == True')) > 0):

                    c2.success("La fournaise est un modèle admissible.")

                    verif_duo_exp = c2.expander(
                        "Suggestion de condenseurs pour la fournaise séléctionnée.")
                    verif_duo_exp.write(phraseAccompagnement(
                        "condenseurs", df_fournaise))  # compléter texte + tableau

                    # Ajout tableau des condenseur qui pourraient matcher
                    condenseur = pd.DataFrame(
                        df_fournaise['Condenseur'].unique().tolist())
                    condenseur.columns = ['Condenseur']
                    verif_duo_exp.dataframe(
                        condenseur, use_container_width=True)
                    verif_duo_exp.write("")
                    verif_duo_exp.write(
                        '_Attention : bien valider la sélection complète_')

                    verif_duo_exp = c2.expander(
                        "Suggestion d'évaporateurs pour la fournaise sélectionnée.")

                    verif_duo_exp.write(
                        phraseAccompagnement('évaporateurs', df_fournaise))

                    # Ajout tableau des évaporateurs qui pourraient matcher
                    evap = pd.DataFrame(
                        df_fournaise['Evaporateur'].unique().tolist())
                    evap.columns = ['Évaporateur']
                    verif_duo_exp.dataframe(evap, use_container_width=True)
                    verif_duo_exp.write("")
                    verif_duo_exp.write(
                        '_Attention : bien valider la sélection complète_')

    if submit_AHRI:

        c2.title("Vérification par numéro AHRI")

        df_AHRI = (df_CEE
                   .query(f"AHRI=={num_AHRI}")
                   .drop(['Condenseur_Prep', 'Evaporateur_Prep', 'Fournaise_Prep'], axis=1)
                   .drop_duplicates()
                   .reset_index(drop=True))

        if df_AHRI.empty:
            c2.error(':warning:  Aucun résultat pour ce numéro AHRI')
        else:
            c2.success(
                ":white_check_mark:  Combinaison trouvée pour ce numéro AHRI")
            c2.dataframe(df_AHRI, use_container_width=True)

            # Bouton Download AHRI
            df_temp = (df_AHRI
                       .sort_values('AHRI')
                       .reset_index(drop=True)
                       )
            df_temp.at[0, 'AHRI Proposé'] = num_AHRI
            df_temp.at[0, 'Vérifié le'] = datetime.now()
            c2.download_button(
                label="📥 Télécharger résultats AHRI",
                data=to_excel(df_temp, 'AHRI'),
                file_name='resultat_AHRI.xlsx')


if __name__ == "__main__":
    main()
