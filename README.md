# brief12
Prediction prix voiture via machine learning

Le code est une application Streamlit pour explorer et analyser un dataset de ventes de voitures, appliquer des prédictions basées sur un modèle machine learning, et permettre le téléchargement de données modifiées. Voici un résumé des principales fonctionnalités :

1. Chargement et Préparation des Données
Chargement du CSV : Le fichier carssales.csv est chargé dans un DataFrame Pandas.
Traitement des données :
Conversion des dates en format datetime sans timezone.
Transformation de la colonne "constructeur" en type category pour des performances améliorées.
Les données peuvent être filtrées et triées dynamiquement via une interface utilisateur Streamlit.

2. Exploration des Données
Filtrage et tri :
Utilisation de divers filtres basés sur le constructeur, le modèle, la gamme de prix, et d'autres colonnes numériques, catégoriques, ou de date.
Les données peuvent être regroupées et agrégées (moyenne, somme, minimum, maximum) selon des colonnes sélectionnées par l'utilisateur.
Interface utilisateur :
L'utilisateur peut interagir via des cases à cocher, des sélections, et des sliders pour modifier l'affichage des données.
Une option pour télécharger les données filtrées en CSV est disponible.

3. Modèle Machine Learning
Chargement des modèles :
Un modèle de régression (fichier model_pkl) est chargé pour prédire les prix.
Un pipeline de prétraitement (model_pipeline) est utilisé pour transformer les nouvelles données utilisateur avant la prédiction.
Prédictions dynamiques :
L'utilisateur entre des informations sur une voiture (année, kilométrage, condition, marque, et modèle).
Ces données sont transformées par le pipeline, et le modèle prédit le prix estimé de la voiture.

4. Fonctionnalités Interactives
Exploration des données : L'utilisateur peut visualiser et filtrer les données selon ses besoins.
Prédiction de prix : Une interface intuitive permet d’estimer le prix d’une voiture.
Téléchargement des résultats : L'utilisateur peut télécharger les données modifiées après filtrage ou tri.
Structure de l'application :
Section d'exploration des données :
Filtrage, tri et regroupement des données existantes.
Téléchargement des données filtrées.
Section de prédiction de prix :
Entrée des caractéristiques d'une voiture.
Prédiction dynamique basée sur le modèle ML.

Ce code combine des éléments d'analyse de données, d'interactivité, et de machine learning pour créer une interface utilisateur conviviale permettant à l'utilisateur de travailler sur des données de ventes de voitures de manière intuitive et informative.






