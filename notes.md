# À faire

## Besoin d'améliorer et tester la recherche, surtout pour les termes avec des '(' et '-'

-[x] Créer une fonction, vérifier si possible d'accélérer... -[x] Tester le système avec les cas compliqués

## Besoin de faire recherche similaire en parallèle avec NEEP

- importer données
- faire recherche
- sortir les résultats
  - si la recherche est un succès
  - proposition d'appareils si non

## Potentiel de faire une application dans le style Streamlit

- déploy avec Github sur Streamlit Cloud
  https://towardsdatascience.com/deploy-a-public-streamlit-web-app-for-free-heres-how-bf56d46b2abe#:~:text=1.3.&text=To%20launch%20the%20app%20locally,full%20path%20to%20the%20file.

Exemple intéressant avec menu déroulant (st.expander)

https://data-science-at-swast-handover-poc-handover-yfa2kz.streamlitapp.com/

[GitHub - Data-Science-at-SWAST/handover_poc: Proof of Concept for Handover Reporting](https://github.com/Data-Science-at-SWAST/handover_poc)

# Vérif Énergy Star

-[x] Si vérifié avec CEE, on doit avoir Labeled ENERGY STAR = YES
_Normalement, j'ai importé seulement ceux identifié Yes_
--> OK

Si vérifié dans la liste du NEEP, on assume Energy star. (NEEP > Energy Star)

- Besoin d'une autorisation pour downloader fichier, en attente
- Sinon, vérifier avec JSébastien s'ils ont la liste complète du MERN ?

### Référence emoji

https://www.webfx.com/tools/emoji-cheat-sheet/

## Requirements

Fichier requirements.txt
https://stackoverflow.com/questions/66899666/how-to-install-from-requirements-txt

## Authentification

Si besoin d'ajouter un processus d'authentification, une librairie existe : streamlit-authentificator
https://youtu.be/JoFGrSRj4X4

## Docker

Exemple pour créer un Docker

https://www.section.io/engineering-education/how-to-deploy-streamlit-app-with-docker/

### Commandes Docker:

#### Image locale

`docker build -t brunoelgrande/recherchebienergie:0.x .`

`docker run -p 8501:8501 recherchebienergie:0.x`

Pour pousser vers Docker Hub
`docker push brunoelgrande/recherchebienergie:0.x`

#### Images vers Docker Hub

`docker login --username=brunoelgrande`

Pour pousser vers Docker Hub avec un build ARM64 et AMD64 (pas d'image locale)
`docker buildx build --platform linux/amd64,linux/arm64 -t brunoelgrande/recherchebienergie:X.X.X --push .`

    Ref: https://medium.com/geekculture/docker-build-with-mac-m1-d668c802ab96

    Step 1
    We will need to create a “builder”. I will call it mybuilder.

    `docker buildx create --name mybuilder`

    Step 2
    Then we tell buildx to use mybuilder.

    `docker buildx use mybuilder`
