import streamlit as st
import pandas as pd
import streamlit_folium as stf
import folium
from folium.plugins import MarkerCluster

# Ajoutez une variable globale pour stocker les pays sélectionnés
selected_countries = []

# Charger les données depuis un fichier CSV
def get_data_map():
    with st.spinner(text='Loading...'):
        df = pd.read_csv("train_stations_europe.csv")
        return df

# Fonction pour afficher la carte
def show_map(data, selected_countries):
    with st.spinner(text='Loading...'):
        multiselect_key_map_countries = f"map_multiselect_countries_{id(show_map)}"
        # Utilisez st.multiselect pour obtenir les pays sélectionnés
        selected_countries = st.sidebar.multiselect('Sélectionnez les pays', data['country'].unique(), key=multiselect_key_map_countries)

        # Filtrer les données en fonction des pays sélectionnés
        data_filtered = data[data['country'].isin(selected_countries)]

        # Supprimer les lignes avec des valeurs manquantes dans latitude et longitude
        data_cleaned = data_filtered.dropna(subset=["latitude", "longitude"])

        # Vérifier si la DataFrame après le nettoyage est vide
        if data_cleaned.empty:
            st.warning("Aucune donnée disponible après le nettoyage. Sélectionnez d'autres pays.")
            return selected_countries

        # Créer une carte Folium centrée sur la moyenne des coordonnées
        trainmap = folium.Map(location=[data_cleaned["latitude"].mean(), data_cleaned["longitude"].mean()], zoom_start=5)

        # Créer un cluster de marqueurs
        marker_cluster = MarkerCluster().add_to(trainmap)

        # Ajouter des marqueurs pour chaque point
        for index, row in data_cleaned.iterrows():
            folium.Marker([row["latitude"], row["longitude"]], popup=row['name_norm']).add_to(marker_cluster)

        # Afficher la carte dans Streamlit
        stf.folium_static(trainmap)

        return selected_countries


def main():
    st.markdown(
    "<h1 style='text-align: left; font-size: 1em;'>Carte représentant les principales gares ferroviaires et de métro en Europe</h1>",
    unsafe_allow_html=True,
)

    # Charger les données
    data = get_data_map()

    # Afficher la carte avec les points
    show_map(data, selected_countries)

if __name__ == "__main__":
    main()
