# Importation des bibliothèques nécessaires 
import streamlit as st
import pandas as pd
import plotly.express as px

# Fonction pour charger les données provenant du CSV
def get_data_places():
    with st.spinner(text='Chargement...'):
        df = pd.read_csv("rail_eq_pa_csb_linear.csv")

        # Filtrage des données dans le fichier CSV
        seat = df["seat"].unique()
        countries = df["geo"].unique()
        years = df["TIME_PERIOD"].unique()
        value = df["OBS_VALUE"].unique()

    return (df, seat, countries, years, value)

def graph_places():
    # Fonction pour créer le graphique de l'évolution du nombre de places dans les trains au fil des années

    # Appel de la fonction pour obtenir les données
    data = get_data_places()
    sorted_years = sorted(data[3])

    # Widgets pour sélectionner les paramètres du graphique
    selected_countries_places = st.sidebar.multiselect('Sélectionnez les pays', data[2])
    selected_seat_places = st.sidebar.selectbox('Sélectionnez le type de siège', data[1])
    selected_begin_places = st.sidebar.select_slider('Date de début', sorted_years, value=min(sorted_years))
    selected_end_places = st.sidebar.select_slider('Date de fin', sorted_years, value=max(sorted_years))

    # Filtrage des données en fonction des pays, du type de place et de la plage d'année sélectionnée
    filtered_data = data[0][(data[0]['geo'].isin(selected_countries_places)) &
                            (data[0]['seat'] == selected_seat_places) &
                            (data[0]['TIME_PERIOD'] >= selected_begin_places) &
                            (data[0]['TIME_PERIOD'] <= selected_end_places)]

    # Création du graphique avec Plotly Express
    if not filtered_data.empty:
        # Tracé 'scatter' (les points) pour les données individuelles
        fig = px.scatter(filtered_data, x='TIME_PERIOD', y='OBS_VALUE', color='geo',
                        labels={'OBS_VALUE': 'Nombre de places (en miliers)', 'TIME_PERIOD': 'Année', 'geo': 'Pays'},
                        title='Evolution du nombre de places dans les trains au fil des années',
                        color_discrete_sequence=px.colors.qualitative.Set1)  # Définition la palette de couleurs

        # Tracé 'line' (ligne qui relie les données) pour les données agrégées par pays
        countries_years_data = filtered_data.groupby(['geo', 'TIME_PERIOD']).agg({'OBS_VALUE': 'sum'}).reset_index()
        line_fig = px.line(countries_years_data, x='TIME_PERIOD', y='OBS_VALUE', color='geo', color_discrete_sequence=px.colors.qualitative.Set1)  # Utiliser la même palette de couleurs

        # Mise à jour du tracé 'line' avec le tracé 'scatter' et masquage de la légende pour 'line' pour éviter une légende inutile
        for trace in line_fig['data']:
            trace['showlegend'] = False
            fig.add_trace(trace)

        # Affichage d'un avertissement pour les pays sans données
        countries_without_data = [country for country in selected_countries_places if country not in countries_years_data['geo'].unique()]
        if countries_without_data:
            st.warning(f"Aucune donnée enregistrée pour {', '.join(countries_without_data)} à l'année sélectionnée.")

        st.plotly_chart(fig)
        
    # Ajout d'un message lorsqu'aucune données n'est sélectionné dans un des widgets
    else:
        st.warning("Aucune donnée sélectionnée. Veuillez choisir au moins un pays, un type de siège et une plage d'années valable.")

def places_TarteAuFromage():
    # Fonction pour créer le graphique de comparaisons des différents types de place au sein du même pays pour une année précise

    # Appel de la fonction pour obtenir les données
    data = get_data_places()
    sorted_years = sorted(data[3])

    # Widgets pour sélectionner les paramètres du graphique
    selected_countries_places = st.sidebar.selectbox('Sélectionnez les pays', data[2])
    selected_begin_places = st.sidebar.select_slider('Année à observer', sorted_years, value=min(sorted_years))
    selected_seat_places = ['Première classe', 'Deuxième classe']

    # Filtrage des données en fonction du pays, l'année et du type de place sélectionné
    filtered_data = data[0][(data[0]['geo'] == selected_countries_places) &
                            (data[0]['TIME_PERIOD'] >= selected_begin_places) &
                            (data[0]['seat'].isin(selected_seat_places))]

    # Création du Piechart avec Plotly Express
    if not filtered_data.empty:
        fig = px.pie(filtered_data, names='seat', values='OBS_VALUE', title=f"Répartition des sièges pour {selected_countries_places}",
                     labels={'seat': 'Type de siège'}, hole=0.4)
        st.plotly_chart(fig)
        
    # Ajout d'un message lorsqu'aucune données n'est sélectionné dans un des widgets
    else:
        st.warning(f"Aucune donnée disponible pour {selected_countries_places} à l'année {selected_begin_places}.")