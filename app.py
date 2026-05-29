import streamlit as st
import requests
import uuid
import PyPDF2
import io

# URL du Webhook n8n - Idéalement à mettre dans st.secrets pour la sécurité
WEBHOOK_URL = "http://localhost:5678/webhook-test/4e1559f5-1f94-44d9-bf8a-a18b0a424690"
TIMEOUT = 180 

# Configuration de la page : Style épuré pour le dashboard
st.set_page_config(page_title="SMA Clean Code Mentor", page_icon="🛡️", layout="wide")

# Maintien de l'état de session pour suivre les utilisateurs de manière unique
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

st.title("🛡️ SMA Clean Code Mentor")
st.markdown("### Analyse Automatisée (Multi-format : py, js, sql, pdf)")

# Sidebar : Interface de chargement des fichiers
uploaded_file = st.sidebar.file_uploader("Charger un fichier", type=["py", "js", "sql", "pdf"])

if uploaded_file:
    # --- LOGIQUE D'EXTRACTION ---
    # On différencie le traitement binaire (PDF) du traitement texte (Code)
    try:
        if uploaded_file.name.endswith(".pdf"):
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            # Concaténation de tout le texte extrait pour analyse LLM
            content = "\n".join([page.extract_text() for page in pdf_reader.pages])
        else:
            # Décodage robuste des fichiers texte
            content = uploaded_file.read().decode("utf-8", errors="ignore")
        
        st.sidebar.success(f"Fichier chargé : {uploaded_file.name}")
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier : {e}")
        st.stop()

    # --- ACTION D'ANALYSE ---
    if st.button("Lancer l'Analyse IA"):
        with st.spinner("Analyse approfondie en cours (Reviewer -> Orchestrateur -> Documenteur)..."):
            # Préparation du payload envoyé vers l'orchestrateur n8n
            payload = {
                "code": content, 
                "fileName": uploaded_file.name,
                "sessionId": st.session_state.session_id
            }

            try:
                # Appel POST vers l'API n8n
                response = requests.post(WEBHOOK_URL, json=payload, timeout=TIMEOUT)

                if response.status_code == 200:
                    data = response.json()
                    # Extraction des données renvoyées par le workflow n8n
                    rapport = data.get("rapport") or data.get("report") or "Aucun rapport."
                    score = data.get("score") or "0"
                    
                    # --- AFFICHAGE DES RÉSULTATS ---
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown("### 📋 Rapport de Review")
                        st.write(rapport) # Rendu du Markdown généré par l'IA
                    with col2:
                        st.markdown("### 🏆 Score Final")
                        st.metric("Note", f"{score}/10")
                else:
                    # Gestion explicite des erreurs HTTP
                    st.error(f"Erreur serveur n8n (Code {response.status_code}). Vérifiez si le workflow est actif.")
            except Exception as e:
                # Gestion des timeouts ou erreurs réseau
                st.error(f"Erreur de connexion : {e}. Assurez-vous que le serveur n8n répond.")

st.sidebar.markdown("---")
st.sidebar.info("Projet CleanCode-Swarm IA | SMA 2026")