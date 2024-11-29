import logging
from dto.connexion import Connexion
from model.prompt import Prompt
from model.utilisateur import Utilisateur

# Configuration du logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Service_Traducteur(Connexion):

    @classmethod
    def sauvegarder_prompt(cls, prompt: Prompt):
        logger.debug("Début de la méthode sauvegarder_prompt")

        # Log des données du prompt reçues
        logger.debug(f"Paramètres reçus - Texte à traduire : {prompt.atraduire}, Traduction : {prompt.traduction}, "
                    f"Version : {prompt.version}, Utilisateur : {prompt.utilisateur}")

        # Conversion de 'prompt.traduction' si c'est une liste
        if isinstance(prompt.traduction, list):
            prompt.traduction = ", ".join([item.get('translation_text', '') for item in prompt.traduction])
            logger.debug(f"Traduction convertie en texte : {prompt.traduction}")

        cls.ouvrir_connexion()
        logger.debug("Connexion à la base de données ouverte.")

        query = "INSERT INTO Prompts (text_in, text_out, version, utilisateur) VALUES (%s, %s, %s, %s)"
        values = [prompt.atraduire, prompt.traduction, prompt.version, prompt.utilisateur]

        # Log avant l'exécution de la requête
        logger.debug(f"Préparation de la requête : {query} avec les valeurs : {values}")

        try:
            cls.cursor.execute(query, values)
            logger.debug("Requête exécutée avec succès.")
            cls.bdd.commit()
            logger.debug("Transaction validée.")
        except Exception as e:
            logger.error(f"Erreur lors de l'exécution de la requête : {e}")
            cls.bdd.rollback()
        finally:
            cls.fermer_connexion()
            logger.debug("Connexion à la base de données fermée.")
        
        logger.debug("Fin de la méthode sauvegarder_prompt")


    
    @classmethod
    def verifier_login(cls, utilisateur: Utilisateur):
        logger.debug("Début de la méthode verifier_login")
        try:
            cls.ouvrir_connexion()
            logger.debug("Connexion à la base de données ouverte.")
            
            query = "SELECT id, login, mdp FROM utilisateurs WHERE login=%s AND mdp=%s"
            values = [utilisateur.login, utilisateur.mdp]
            logger.debug(f"Exécution de la requête : {query} avec valeurs : {values}")
            
            cls.cursor.execute(query, values)
            result = cls.cursor.fetchone()
            logger.debug(f"Résultat de la requête : {result}")

            if result:
                utilisateur.id = result['id']
                utilisateur.authentifie = True
                logger.info(f"Authentification réussie pour l'utilisateur : {utilisateur.login}")
        except Exception as e:
            logger.error(f"Une erreur inattendue est survenue : {e}")
        finally:
            cls.fermer_connexion()
            logger.debug("Connexion à la base de données fermée.")
            logger.debug("Fin de la méthode verifier_login")

    @classmethod
    def lister_prompts(cls, utilisateur: int):
        logger.debug("Début de la méthode lister_prompts")
        prompts = []

        cls.ouvrir_connexion()
        logger.debug("Connexion à la base de données ouverte.")
        
        query = "SELECT * FROM prompts WHERE utilisateur=%s"
        values = [utilisateur]
        logger.debug(f"Exécution de la requête : {query} avec valeurs : {values}")
        
        cls.cursor.execute(query, values)
        logger.debug("Requête exécutée avec succès.")

        for prompt_lu in cls.cursor:
            logger.debug(f"Lecture d'un prompt : {prompt_lu}")
            prompt = Prompt(
                atraduire=prompt_lu["text_in"],
                traduction=prompt_lu["text_out"],
                version=prompt_lu["version"],
                utilisateur=prompt_lu["utilisateur"]
            )
            prompts.append(prompt)

        cls.fermer_connexion()
        logger.debug("Connexion à la base de données fermée.")
        logger.debug("Fin de la méthode lister_prompts")
        
        return prompts
