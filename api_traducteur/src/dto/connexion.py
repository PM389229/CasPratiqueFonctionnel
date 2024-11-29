import mysql.connector as mysqlpyth
import logging

from config.parametres import BDD_USER, BDD_PASSWORD, BDD_HOST, BDD_PORT, BDD_DATABASE

logging.basicConfig(level=logging.DEBUG)

class Connexion:

    @classmethod
    def ouvrir_connexion(cls):
        logging.debug(f"Connexion à la base {BDD_DATABASE} sur {BDD_HOST}:{BDD_PORT} avec {BDD_USER}/{BDD_PASSWORD}")
        cls.bdd = mysqlpyth.connect(
            user=BDD_USER,
            password=BDD_PASSWORD,
            host=BDD_HOST,
            port=BDD_PORT,
            database=BDD_DATABASE
        )
        cls.cursor = cls.bdd.cursor(dictionary=True)
        logging.debug("Connexion établie.")

    @classmethod
    def fermer_connexion(cls):
        logging.debug("Fermeture du curseur et de la connexion.")
        cls.cursor.close()
        logging.debug("Curseur fermé.")
        cls.bdd.close()
        logging.debug("Connexion fermée.")
