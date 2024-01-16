# power.py

import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

def get_data_power():
    with st.spinner(text='Loading...'):
        df = pd.read_csv("rail_eq_locop_linear.csv")

        # Filtrer les donnees
        motor_energy = df["mot_nrg"].unique()
        vehicle = df["vehicle"].unique()
        countries = df["geo"].unique()
        years = df["TIME_PERIOD"].unique()
        value = df["OBS_VALUE"].unique()

    return (df, motor_energy, vehicle, countries, years, value)

def graph_power():
    # Appeler la fonction pour obtenir les données
    data = get_data_power()
    sorted_years = sorted(data[4])

    # Widget to select countries
    selected_countries_power = st.sidebar.multiselect('Sélectionnez les pays', data[3])
    selected_motor_power = st.sidebar.selectbox('Sélectionnez un type de moteur', data[1])
    selected_year_power = st.sidebar.select_slider('Sélectionnez une année', sorted_years, value=min(sorted_years))

    # Assurer que selected_motor_power est une liste
    selected_motor_power_list = [selected_motor_power] if isinstance(selected_motor_power, str) else selected_motor_power

    # Filtrer les données en fonction des pays, du type de moteur et de l'année sélectionnée
    filtered_data = data[0][(data[0]['geo'].isin(selected_countries_power)) &
                            (data[0]['TIME_PERIOD'] == selected_year_power) &
                            (data[0]['mot_nrg'].isin(selected_motor_power_list))]

    # Vérifier si des données sont sélectionnées
    if not filtered_data.empty:
        # Préparer les données pour le tracé des barres
        countries_years_data = filtered_data.groupby(['geo']).agg({'OBS_VALUE': 'sum'}).reset_index()

        # Créer le graphique de comparaison des pays avec Altair
        chart = alt.Chart(countries_years_data).mark_bar().encode(
            x=alt. X('geo:N', title='Pays'),
            y=alt.Y('OBS_VALUE:Q', title='Puissance (en MW)'),
            color=alt.Color('geo:N', title='Pays', scale=alt.Scale(scheme='category10')),
        ).properties(
            width=800,
            height=500
        )

        

        # Afficher un avertissement pour les pays sans données
        countries_without_data = [country for country in selected_countries_power if country not in countries_years_data['geo'].unique()]
        if countries_without_data:
            st.warning(f"Aucune donnée enregistrée pour {', '.join(countries_without_data)} à l'année sélectionnée.")
            
        st.altair_chart(chart)
    else:
        st.warning("Aucune donnée sélectionnée. Veuillez choisir au moins un pays, un type de moteur et une année.")


def graph_power_time():
    # Appeler la fonction pour obtenir les données
    data = get_data_power()

    # Ajouter le bouton pour masquer/afficher les maximas
    show_winner = st.checkbox("Afficher le vainqueur")

    # Logique en fonction de l'état du bouton "Afficher le vainqueur"
    # Cas où le bouton est activé
    if show_winner == True:
        st.info("N'oubliez pas de sélectionner plusieurs pays pour afficher le vainqueur.", icon="ℹ️")
    # Cas où le bouton est désactivé
    selected_countries_power = st.sidebar.selectbox('Sélectionnez un pays', data[3])
    selected_vehicles_power = st.sidebar.radio('Sélectionnez un type de véhicule', data[2])
    selected_motors_power = st.sidebar.multiselect('Sélectionnez un type de moteur', data[1])

    # Appliquer les conditions logiques pour obtenir les données finales
    filtered_data = data[0][(data[0]['geo'].isin([selected_countries_power])) &
                            (data[0]['vehicle'].isin([selected_vehicles_power])) &
                            (data[0]['mot_nrg'].isin(selected_motors_power))]

    # Créer le graphique avec Plotly Express
    if not filtered_data.empty:
        # Tracé 'scatter' pour les données individuelles
        fig = px.scatter(filtered_data, x='TIME_PERIOD', y='OBS_VALUE', color='mot_nrg',
                        labels={'OBS_VALUE': 'Puissance (en MW)', 'TIME_PERIOD': 'Année', 'geo': 'Pays'},
                        title=(f'Evolution de la puissance des {selected_vehicles_power.lower()} en {selected_countries_power} par an, par type de véhicule et de moteur'),
                        color_discrete_sequence=px.colors.qualitative.Set1)  # Définir la palette de couleurs

        # Tracé 'line' pour les données agrégées par pays
        countries_years_data_vehicle = filtered_data.groupby(['vehicle', 'TIME_PERIOD']).agg({'OBS_VALUE': 'sum'}).reset_index()
        countries_years_data_motnrg = filtered_data.groupby(['mot_nrg', 'TIME_PERIOD']).agg({'OBS_VALUE': 'sum'}).reset_index()

        # Utiliser color='mot_nrg' pour le tracé de lignes également
        line_fig_vehicle = px.line(countries_years_data_vehicle, x='TIME_PERIOD', y='OBS_VALUE', color='vehicle')
        line_fig_motnrg = px.line(countries_years_data_motnrg, x='TIME_PERIOD', y='OBS_VALUE', color='mot_nrg', color_discrete_sequence=px.colors.qualitative.Set1)

        # Mettre à jour le tracé 'line' avec le tracé 'scatter' et masquer la légende pour 'line'
        for trace in line_fig_motnrg['data']:
            trace['showlegend'] = False
            fig.add_trace(trace)


        # Ajouter une annotation pour afficher les informations à droite de la barre
        if show_winner == True:
            max_value_row = filtered_data.loc[filtered_data['OBS_VALUE'].idxmax()]
            fig.add_annotation(x=max_value_row['TIME_PERIOD'],
                   y=max_value_row['OBS_VALUE'],
                   text=f"C'est le {max_value_row['mot_nrg']} qui l'emporte <br> avec {max_value_row['OBS_VALUE']:.0f} MW au maximum",
                   showarrow=True,
                   arrowhead=6,
                   arrowsize=1,
                   arrowwidth=1,
                   arrowcolor='black',
                   ax=0,
                   ay=-50)

        st.plotly_chart(fig)
    else:
        st.warning("Aucune donnée sélectionnée. Veuillez choisir au moins un pays, un type de véhicule et un type de moteur.")
