# traducteur_app.py
import streamlit as st
from streamlit_chat import message
from config.parametres import URL_TRADUCTEUR, URL_VERSIONS, URL_LOGIN, URL_TRADUCTIONS
import requests
import logging
import time

# Configurer le logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TraducteurApp:
    def __init__(self):
        self.URL_TRADUCTEUR = URL_TRADUCTEUR
        self.URL_VERSIONS = URL_VERSIONS
        self.URL_LOGIN = URL_LOGIN
        self.URL_TRADUCTIONS = URL_TRADUCTIONS
        self.titre = "Traducteur"

        # Log des URLs configurées
        logger.info(f"URL_TRADUCTEUR: {self.URL_TRADUCTEUR}")
        logger.info(f"URL_VERSIONS: {self.URL_VERSIONS}")
        logger.info(f"URL_LOGIN: {self.URL_LOGIN}")
        logger.info(f"URL_TRADUCTIONS: {self.URL_TRADUCTIONS}")

        st.set_page_config(
            page_title="Traducteur",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded",
        )

        if "logged_in" not in st.session_state:
            st.session_state["logged_in"] = None

        logger.info("Initialisation de l'application terminée.")
        self.show_login_form()
        self.show_app()




    def show_login_form(self):
        # On  ne va pas afficher le formulaire si l'utilisateur est connecté
        if st.session_state.get("logged_in"):
            # On affiche un message indiquant que l'utilisateur est connecté
            st.sidebar.write(f"Connecté en tant que : {st.session_state['logged_in']}")
            return

        # Fonction pour traiter la connexion
        def login(username, password):
            logger.info(f"Tentative de connexion pour l'utilisateur : {username}")
            data = {"login": username, "mdp": password}

            try:
                response = requests.post(self.URL_LOGIN, json=data)
                logger.info(f"Réponse de l'API login : {response.status_code} - {response.text}")

                if response.status_code == 200:
                    response_login = response.json()
                    if response_login["authentifié"]:
                        st.session_state["logged_in"] = response_login["id"]
                        logger.info(f"L'utilisateur {username} est connecté avec ID : {st.session_state['logged_in']}")
                    else:
                        st.session_state["logged_in"] = None
                        logger.warning("Nom d'utilisateur ou mot de passe incorrect.")
                        st.sidebar.error("Nom d'utilisateur ou mot de passe incorrect.")
                else:
                    st.sidebar.error("Erreur lors de la connexion.")
            except requests.exceptions.RequestException as e:
                st.session_state["logged_in"] = None
                logger.error(f"Erreur réseau : {e}")
                st.sidebar.error("Erreur réseau. Impossible de se connecter.")

        # Formulaire de connexion dans la barre latérale
        st.sidebar.title("Connexion")
        # On ajoute des clés uniques aux widgets pour éviter le conflit d'identifiants 
        username = st.sidebar.text_input("Nom d'utilisateur", key="login_username")
        password = st.sidebar.text_input("Mot de passe", type="password", key="login_password")
        st.sidebar.button("Se connecter", on_click=login, args=(username, password))




        

    def show_index(self):
        st.title(self.titre)
        st.write("Veuillez vous connecter pour accéder aux fonctionnalités sécurisées.")
        logger.info("Affichage de l'écran d'accueil pour les utilisateurs non connectés.")
        
    def show_logout_button(self):
        def logout():
            st.session_state["logged_in"] = None
            logger.info("Déconnexion réussie.")

        st.sidebar.title("Déconnexion")
        st.sidebar.button("Se déconnecter", on_click=logout)    



    def show_app(self):
        if st.session_state.get("logged_in") is None:
            self.show_index()  # Redirection vers la page d'accueil si non connecté
            return

        # Affichage du bouton de déconnexion dans la barre latérale
        with st.sidebar:
            if st.sidebar.button("Déconnexion"):  # Texte mis à jour 
                st.session_state["logged_in"] = None
                st.experimental_rerun()  # Rechargement de l'application après déconnexion

        st.title(self.titre)
        versions = self.get_versions()

        option = st.sidebar.selectbox(
            "Choisissez la traduction à réaliser :",
            versions
        )

        self.add_form(option)

        if st.session_state["logged_in"]:
            logger.info("Utilisateur connecté, affichage du chat.")
            self.add_chat()








    def get_versions(self):
        logger.info("Appel de l'API pour récupérer les versions de traduction.")
        versions = ["Aucune langue détectée !"]
        
        try:
            start_time = time.time()  # Début du chronométrage
            response = requests.get(self.URL_VERSIONS)
            end_time = time.time()  # Fin du chronométrage
            logger.info(f"Réponse de l'API versions : {response.status_code} en {end_time - start_time:.2f} secondes")

            if response.status_code == 200:
                try:
                    versions = response.json()
                    logger.debug(f"Versions disponibles : {versions}")
                except ValueError as e:
                    logger.error(f"Erreur de décodage JSON : {e}")
                    st.error("Erreur lors de la récupération des versions.")
            else:
                logger.error(f"Erreur HTTP : {response.status_code}")
                st.error(f"Erreur : {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur réseau lors de l'appel à /versions : {e}")
            st.error("Erreur réseau. Veuillez vérifier votre connexion.")
        
        return versions



    def add_form(self, option):
        st.subheader(option)
        atraduire = st.text_input("Texte à traduire")

        # Vérifiez si l'utilisateur est connecté
        if st.session_state.get("logged_in") is None:
            st.error("Veuillez vous connecter pour effectuer une traduction.")
            logger.warning("Un utilisateur non connecté a tenté de traduire un texte.")
            return

        # Vérifiez si une version est sélectionnée
        if not option:
            st.error("Veuillez sélectionner une version de traduction.")
            return

        if st.button("Traduire"):
            logger.info(f"Demande de traduction pour le texte : '{atraduire}' avec l'option : {option}")
            
            data = {
                "atraduire": atraduire,
                "version": option,
                "utilisateur": st.session_state["logged_in"]
            }
            
            # Log des données envoyées à l'API
            logger.info(f"Données envoyées à l'API : {data}")

            try:
                start_time = time.time()  # Début du chronométrage
                response = requests.post(self.URL_TRADUCTEUR, json=data)
                end_time = time.time()  # Fin du chronométrage
                logger.info(f"Réponse de l'API traduction en {end_time - start_time:.2f} secondes")


                if response.status_code == 200:
                    reponse = response.json()["traduction"]
                    st.success("Voici votre traduction !")
                    st.write(reponse)
                    logger.info(f"Traduction réussie : {reponse}")
                else:
                    logger.error(f"Erreur HTTP : {response.status_code} - {response.text}")
                    st.error(f"Erreur : {response.status_code}")
                    st.write("Détails de l'erreur :", response.text)
            except requests.exceptions.RequestException as e:
                logger.error(f"Erreur réseau lors de la demande de traduction : {e}")
                st.error("Erreur réseau. Veuillez vérifier votre connexion.")





    def add_chat(self):
        url = f"{self.URL_TRADUCTIONS}{st.session_state['logged_in']}"
        logger.info(f"Récupération des traductions pour l'utilisateur ID {st.session_state['logged_in']} via {url}")

        chat = requests.get(url)
        logger.info(f"Réponse de l'API chat : {chat.status_code} - {chat.text}")

        if chat.status_code == 200:
            chat_messages = chat.json()
            logger.info(f"Nombre de traductions récupérées pour l'utilisateur ID {st.session_state['logged_in']} : {len(chat_messages)}")
            logger.debug(f"Messages récupérés : {chat_messages}")

            for i, prompt in enumerate(chat_messages):
                # Ajoutez une clé unique basée sur l'index (ou un autre identifiant unique)
                message(prompt["atraduire"], is_user=True, key=f"user_msg_{i}")
                message(prompt["traduction"], key=f"bot_msg_{i}")
        else:
            logger.error(f"Erreur lors de la récupération des messages : {chat.status_code}")
            st.error(f"Erreur : {chat.status_code}")
