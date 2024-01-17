# Importation des bibliothèques nécessaires 
import streamlit as st
import pandas as pd
import plotly.express as px

# Fonction pour charger les données provenant du CSV
def get_data_quantity():
    with st.spinner(text='Chargement...'):
        df = pd.read_csv("rail_eq_locon_linear.csv")

        # Filtrage des données dans le fichier CSV
        motor_energy = df["mot_nrg"].unique()
        vehicle = df["vehicle"].unique()
        countries = df["geo"].unique()
        years = df["TIME_PERIOD"].unique()
        value = df["OBS_VALUE"].unique()

    return (df, motor_energy, vehicle, countries, years, value)

def graph_quantity():
    # Appel de la fonction pour obtenir les données
    data = get_data_quantity()


    # Ajout du bouton pour masquer/afficher les vainqueurs
    show_winner = st.checkbox("Afficher le vainqueur")

    # Réaction en fonction de l'état du bouton "Afficher le vainqueur"
    # Cas où le bouton est activé
    if show_winner == True:
        st.info("N'oubliez pas de sélectionner plusieurs pays pour afficher le vainqueur.", icon="ℹ️")
    # Cas où le bouton est désactivé
    selected_countries_quantity = st.sidebar.multiselect('Sélectionnez des pays', data[3])
    selected_vehicles_quantity = st.sidebar.radio('Sélectionnez un type de véhicule', data[2])
    selected_motors_quantity = st.sidebar.selectbox('Sélectionnez un type de moteur', data[1])

    # Filtrage des données en fonction des pays, du type de véhicule et du type de moteur sélectionné
    filtered_data = data[0][(data[0]['geo'].isin(selected_countries_quantity)) &
                            (data[0]['vehicle'].isin([selected_vehicles_quantity])) &
                            (data[0]['mot_nrg'].isin([selected_motors_quantity]))]

    # Création du graphique avec Plotly Express
    if not filtered_data.empty:
        # Tracé 'scatter' (les points) pour les données individuelles
        fig = px.scatter(filtered_data, x='TIME_PERIOD', y='OBS_VALUE', color='geo',
                      labels={'OBS_VALUE': 'Nombre de voitures', 'TIME_PERIOD': 'Année', 'geo': 'Pays'},
                      title=(f'Evolution du nombre de {selected_vehicles_quantity.lower()}s par an'),                        
                      color_discrete_sequence=px.colors.qualitative.Set1)  # Définition la palette de couleurs

        # Tracé 'line' (ligne qui relie les données) pour les données agrégées par pays
        countries_years_data = filtered_data.groupby(['geo', 'TIME_PERIOD']).agg({'OBS_VALUE': 'sum'}).reset_index()
        line_fig = px.line(countries_years_data, x='TIME_PERIOD', y='OBS_VALUE', color='geo', color_discrete_sequence=px.colors.qualitative.Set1)

        # Mise à jour du tracé 'line' avec le tracé 'scatter' et masquage de la légende pour 'line' pour éviter une légende inutile
        for trace in line_fig['data']:
            trace['showlegend'] = False
            fig.add_trace(trace)

        # Affichage d'un avertissement pour les pays sans données
        countries_without_data = [country for country in selected_countries_quantity if country not in countries_years_data['geo'].unique()]
        if countries_without_data:
            st.warning(f"Aucune donnée enregistrée pour {', '.join(countries_without_data)} à l'année sélectionnée.")

        # Ajout d'une annotation pour afficher les informations du vainqueur à droite du point
        if show_winner == True:
            max_value_row = filtered_data.loc[filtered_data['OBS_VALUE'].idxmax()]
            fig.add_annotation(x=max_value_row['TIME_PERIOD'],
                   y=max_value_row['OBS_VALUE'],
                   text=f"Le pays qui en possède / a possédé <br> le plus est le/la {max_value_row['geo']} avec <br> {max_value_row['OBS_VALUE']:.0f} voitures en {max_value_row['TIME_PERIOD']}",
                   showarrow=True,
                   arrowhead=6,
                   arrowsize=1,
                   arrowwidth=1,
                   arrowcolor='black',
                   ax=0,
                   ay=-50)
        st.plotly_chart(fig)
        
    # Ajout d'un message lorsqu'aucune données n'est sélectionné dans un des widgets
    else:
        st.warning("Aucune donnée sélectionnée. Veuillez choisir au moins un pays, un type de véhicule et un type de moteur.")
