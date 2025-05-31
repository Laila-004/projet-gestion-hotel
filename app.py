import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# ------------------------ TITRE ------------------------
st.markdown('<div class="title">Gestion Hôtelière 🏨</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Interface moderne pour gérer vos clients, réservations et chambres.</div>', unsafe_allow_html=True)

# ------------------------ CONNEXION BDD ------------------------
conn = sqlite3.connect("hotel.db")
cursor = conn.cursor()

# ------------------------ MENU ------------------------
menu = [
    "Accueil",
    "Liste des clients",
    "Liste des réservations",
    "Chambres disponibles",
    "Ajouter un client",
    "Ajouter une réservation"
]
choix = st.sidebar.selectbox("📋 Menu", menu)

# ------------------------ PAGES ------------------------
if choix == "Accueil":
    st.success("Bienvenue dans l'application de gestion hôtelière !")

elif choix == "Liste des clients":
    st.subheader("👥 Clients enregistrés")
    df = pd.read_sql_query("SELECT * FROM Client", conn)
    st.dataframe(df, use_container_width=True)

elif choix == "Liste des réservations":
    st.subheader("🗕️ Réservations")
    query = """
    SELECT R.id, C.nom AS client, CH.numero AS chambre, R.date_debut, R.date_fin
    FROM Reservation R
    JOIN Client C ON R.id_client = C.id
    JOIN Chambre CH ON R.id_chambre = CH.id;
    """
    df = pd.read_sql_query(query, conn)
    st.dataframe(df, use_container_width=True)

elif choix == "Chambres disponibles":
    st.subheader("🛏️ Chambres disponibles")
    date_debut = st.date_input("📆 Date de début", value=date.today())
    date_fin = st.date_input("📆 Date de fin", value=date.today())

    if st.button("🔍 Rechercher"):
        query = f"""
        SELECT * FROM Chambre
        WHERE id NOT IN (
            SELECT id_chambre FROM Reservation
            WHERE date_debut <= '{date_fin}' AND date_fin >= '{date_debut}'
        );
        """
        df = pd.read_sql_query(query, conn)
        st.dataframe(df, use_container_width=True)

elif choix == "Ajouter un client":
    st.subheader("➕ Nouveau client")
    nom = st.text_input("Nom")
    adresse = st.text_input("Adresse")
    ville = st.text_input("Ville")
    code_postal = st.number_input("Code postal", step=1)
    email = st.text_input("Email")
    telephone = st.text_input("Téléphone")

    if st.button("✅ Ajouter le client"):
        cursor.execute("""
        INSERT INTO Client (adresse, ville, code_postal, email, telephone, nom)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (adresse, ville, code_postal, email, telephone, nom))
        conn.commit()
        st.success("Client ajouté avec succès.")

elif choix == "Ajouter une réservation":
    st.subheader("➕ Nouvelle réservation")
    id_client = st.number_input("ID client", step=1)
    id_chambre = st.number_input("ID chambre", step=1)
    date_debut = st.date_input("Date de début", value=date.today())
    date_fin = st.date_input("Date de fin", value=date.today())

    if st.button("✅ Ajouter la réservation"):
        cursor.execute("""
        INSERT INTO Reservation (date_debut, date_fin, id_client, id_chambre)
        VALUES (?, ?, ?, ?)
        """, (date_debut, date_fin, id_client, id_chambre))
        conn.commit()
        st.success("Réservation enregistrée avec succès.")
