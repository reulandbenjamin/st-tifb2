# Importation des bibliothèques nécessaires 
import streamlit as st
import pandas as pd
import streamlit_folium as stf
import folium
from folium.plugins import MarkerCluster

# Ajout d'une variable globale pour stocker les pays sélectionnés
selected_countries = []

# Fonction pour charger les données provenant du CSV
def get_data_map():
    with st.spinner(text='Chargement...'):
        df = pd.read_csv("train_stations_europe.csv")
        return df

# Fonction pour afficher la carte
def show_map():
    st.markdown(
    "<h1 style='text-align: left; font-size: 1em;'>Carte représentant les principales gares ferroviaires et de métro en Europe</h1>",
    unsafe_allow_html=True)

    # Chargement les données
    data = get_data_map()

    with st.spinner(text='Chargement...'):

        # Utilisation de st.multiselect pour obtenir les pays sélectionnés
        selected_countries = st.sidebar.multiselect('Sélectionnez les pays', data['country'].unique())

        # Filtrage des données en fonction des pays sélectionnés
        data_filtered = data[data['country'].isin(selected_countries)]

        # Suppression des lignes avec des valeurs manquantes dans latitude et longitude
        data_cleaned = data_filtered.dropna(subset=["latitude", "longitude"])

        # Vérification si la DataFrame après le nettoyage est vide et renvoie d'un message si c'est la cas
        if data_cleaned.empty:
            st.warning("Aucune donnée disponible après le nettoyage. Sélectionnez d'autres pays.")
            return selected_countries

        # Création d'une carte Folium centrée sur la moyenne des coordonnées
        trainmap = folium.Map(location=[data_cleaned["latitude"].mean(), data_cleaned["longitude"].mean()], zoom_start=5)

        # Création de clusters de marqueurs (groupement des gares pour la lisibilité de la carte)
        marker_cluster = MarkerCluster().add_to(trainmap)

        # Ajout des marqueurs pour chaque point
        for index, row in data_cleaned.iterrows():
            folium.Marker([row["latitude"], row["longitude"]], popup=row['name_norm']).add_to(marker_cluster)

        # Affichage de la carte dans Streamlit
        stf.folium_static(trainmap)

        return selected_countries