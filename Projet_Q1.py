import streamlit as st
from power import graph_power, graph_power_time
from quantity import graph_quantity
from places import places_TarteAuFromage, graph_places
from map import main as map_main  # Renommez la fonction main dans map.py pour éviter les conflits de noms

# Titre global
st.title("Analyse des données du réseau ferroviaire en Europe continentale")

# Image dans la sidebar
sidebar_image_path = "https://upload.wikimedia.org/wikipedia/fr/d/de/Logo_HEPL.png"
st.sidebar.markdown(
    "<div style='display: flex; justify-content: center; margin-top: -65px'><img src='{}' width='150'></div>".format(sidebar_image_path),
    unsafe_allow_html=True
)
st.sidebar.markdown(
    "<h1 style='text-align: left; font-size: 1.1em; margin-top: -25px'>Cours de techniques informatiques</h1>",
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    "<h1 style='text-align: left; font-size: 0.85em; margin-top: -35px'>Deuxième bachelier en ingénierie industrielle</h1>",
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    "<h1 style='text-align: left; font-size: 0.75em; margin-top: -35px'>CLOES Maxime  -  REULAND Benjamin</h1>",
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    "<h1 style='text-align: left; font-size: 1em; margin-bottom: -30px'>Menu :</h1>",
    unsafe_allow_html=True,
)

# Options du menu
pages = ["Carte interactive des gares", "Nombre de voitures", "Places dans les trains", "Puissance des locomotives"]
pages_power = ["Puissance par pays","Evolution de la puissance au fil des ans"]
pages_quantity = ["Evolution au fil des années", "Comparaison par classe"]

# Sélection de la page à afficher dans le menu déroulant
selected_page = st.sidebar.selectbox("Sélectionnez une page", pages)

# Réglages spécifiques à chaque page
if selected_page == "Carte interactive des gares":
    st.sidebar.markdown(
    "<h1 style='text-align: left; font-size: 1em; margin-bottom: -30px'>Paramétrage des graphiques :</h1>",
    unsafe_allow_html=True,
)
    map_main()

elif selected_page == "Nombre de voitures":
    st.sidebar.markdown(
    "<h1 style='text-align: left; font-size: 1em; margin-bottom: -30px'>Paramétrage des graphiques :</h1>",
    unsafe_allow_html=True,
)
    graph_quantity()

elif selected_page == "Places dans les trains":
    selected_page_quantity = st.sidebar.selectbox("Sélectionnez une sous-page", pages_quantity)
    st.sidebar.markdown(
    "<h1 style='text-align: left; font-size: 1em; margin-bottom: -30px'>Paramétrage des graphiques :</h1>", unsafe_allow_html=True,)
    if selected_page_quantity == "Evolution au fil des années":
        graph_places()
    else :
        places_TarteAuFromage()

elif selected_page == "Puissance des locomotives":
    selected_page_power = st.sidebar.selectbox("Sélectionnez une sous-page", pages_power)
    st.sidebar.markdown(
    "<h1 style='text-align: left; font-size: 1em; margin-bottom: -30px'>Paramétrage des graphiques :</h1>", unsafe_allow_html=True)
    if selected_page_power == "Puissance par pays":
        st.markdown(
        "<h1 style='text-align: left; font-size: 1em;'>Puissance en MW des voitures de train par pays, en fonction d'une année et du type de moteur</h1>" , unsafe_allow_html=True)
        graph_power()
    else :
        graph_power_time()