# Importation des bibliothèques nécessaires 
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# Fonction pour charger les données provenant du CSV
def get_data_power():
    with st.spinner(text='Chargement...'):
        df = pd.read_csv(R"rail_eq_locop_linear.csv")

        # Filtrage des données dans le fichier CSV
        motor_energy = df["mot_nrg"].unique()
        vehicle = df["vehicle"].unique()
        countries = df["geo"].unique()
        years = df["TIME_PERIOD"].unique()
        value = df["OBS_VALUE"].unique()

    return (df, motor_energy, vehicle, countries, years, value)

def graph_power():
    # Fonction pour créer le graphique de comparaison de puissance par pays
    
    # Appel de la fonction pour obtenir les données
    data = get_data_power()
    sorted_years = sorted(data[4])

    # Widgets pour sélectionner les paramètres du graphique
    selected_countries_power = st.sidebar.multiselect('Sélectionnez les pays', data[3])
    selected_motor_power = st.sidebar.selectbox('Sélectionnez un type de moteur', data[1])
    selected_year_power = st.sidebar.select_slider('Sélectionnez une année', sorted_years, value=min(sorted_years))

    # On s'assure que selected_motor_power est une liste puisque multiselect renvoie seulement une chaine de caractère s'il n'y qu'un seul type de moteur selectionné, ce qui pose problème par la suite
    selected_motor_power_list = [selected_motor_power] if isinstance(selected_motor_power, str) else selected_motor_power

    # Filtrage des données en fonction des pays, du type de moteur et de l'année sélectionné
    filtered_data = data[0][(data[0]['geo'].isin(selected_countries_power)) &
                            (data[0]['TIME_PERIOD'] == selected_year_power) &
                            (data[0]['mot_nrg'].isin(selected_motor_power_list))]

    # Vérification de la sélection des données
    if not filtered_data.empty:
        # Préparation des données pour le tracé des barres si les données sont rentrées
        countries_years_data = filtered_data.groupby(['geo']).agg({'OBS_VALUE': 'sum'}).reset_index()

        # Création du graphique de comparaison des pays avec Altair
        chart = alt.Chart(countries_years_data).mark_bar().encode(
            x=alt. X('geo:N', title='Pays'),
            y=alt.Y('OBS_VALUE:Q', title='Puissance (en MW)'),
            color=alt.Color('geo:N', title='Pays', scale=alt.Scale(scheme='category10')),
        ).properties(
            width=800,
            height=500
        )

        # Affichage d'un avertissement pour les pays sans données
        countries_without_data = [country for country in selected_countries_power if country not in countries_years_data['geo'].unique()]
        if countries_without_data:
            st.warning(f"Aucune donnée enregistrée pour {', '.join(countries_without_data)} à l'année sélectionnée.")
            
        st.altair_chart(chart)
    else:
        st.warning("Aucune donnée sélectionnée. Veuillez choisir au moins un pays, un type de moteur et une année.")

def graph_power_time():
    # Fonction pour créer le graphique de l'évolution de la puissance par pays au cours des années
    
    # Appel de la fonction pour obtenir les données
    data = get_data_power()

    # Ajout du bouton pour masquer/afficher les vainqueurs
    show_winner = st.checkbox("Afficher le vainqueur")

    # Réaction en fonction de l'état du bouton "Afficher le vainqueur"
    # Cas où le bouton est activé
    if show_winner == True:
        st.info("N'oubliez pas de sélectionner plusieurs pays pour afficher le vainqueur.", icon="ℹ️")
    # Cas où le bouton est désactivé
    selected_countries_power = st.sidebar.selectbox('Sélectionnez un pays', data[3])
    selected_vehicles_power = st.sidebar.radio('Sélectionnez un type de véhicule', data[2])
    selected_motors_power = st.sidebar.multiselect('Sélectionnez un type de moteur', data[1])

    # Filtrage des données en fonction des pays, du type de véhicule et du type de moteur sélectionné
    filtered_data = data[0][(data[0]['geo'].isin([selected_countries_power])) &
                            (data[0]['vehicle'].isin([selected_vehicles_power])) &
                            (data[0]['mot_nrg'].isin(selected_motors_power))]

    # Création du graphique avec Plotly Express
    if not filtered_data.empty:
        # Tracé 'scatter' (les points) pour les données individuelles
        fig = px.scatter(filtered_data, x='TIME_PERIOD', y='OBS_VALUE', color='mot_nrg',
                        labels={'OBS_VALUE': 'Puissance (en MW)', 'TIME_PERIOD': 'Année', 'geo': 'Pays'},
                        title=(f'Evolution de la puissance des {selected_vehicles_power.lower()} en {selected_countries_power} par an, par type de véhicule et de moteur'),
                        color_discrete_sequence=px.colors.qualitative.Set1)  # Définition la palette de couleurs

        # Tracé 'line' (ligne qui relie les données) pour les données agrégées par pays
        countries_years_data_motnrg = filtered_data.groupby(['mot_nrg', 'TIME_PERIOD']).agg({'OBS_VALUE': 'sum'}).reset_index()

        # Utilisation de color='mot_nrg' pour le tracé de lignes également
        line_fig_motnrg = px.line(countries_years_data_motnrg, x='TIME_PERIOD', y='OBS_VALUE', color='mot_nrg', color_discrete_sequence=px.colors.qualitative.Set1)

        # Mise à jour du tracé 'line' avec le tracé 'scatter' et masquage de la légende pour 'line' pour éviter une légende inutile
        for trace in line_fig_motnrg['data']:
            trace['showlegend'] = False
            fig.add_trace(trace)

        # Ajout d'une annotation pour afficher les informations du vainqueur à droite du point
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

    # Ajout d'un message lorsqu'aucune données n'est sélectionné dans un des widgets
    else:
        st.warning("Aucune donnée sélectionnée. Veuillez choisir au moins un pays, un type de véhicule et un type de moteur.")
