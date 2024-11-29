# Ticket d'incident 3

## Étapes pour reproduire le problème
1. Saisir l'URL "localhost:8501" et valider pour charger l'application web Traducteur.

## Résultat actuel
L'application affiche le volet de connexion et le traducteur.
Si on se connecte avec le compte **Cleese** / **Sacré Graal!**, il n'y a aucun effet sur la vue.

![Capture d'écran de l'incident](./ressources/ticket3.png)

## Comportement attendu
- Avant l'authentification d'un compte reconnu, l'application doit afficher le volet de connexion et une page d'accueil.
- Après l'authentification d'un compte reconnu, l'application doit afficher le bouton de **déconnexion** et la page du traducteur.
- Lors d'une déconnexion, l'application retrouve son état initial.

Le traducteur ne doit être affiché que pour les comptes utilisateurs authentifiés.




## Rajouts persos

## Activation env virtuel api 
.\venv\Scripts\activate
 (à PS C:\Users\User\Downloads\CoursAlternance\CASPRATIQUE\py-traducteur\api_traducteur>)

## docs et commande pour api

python api.py dans : PS C:\Users\User\Downloads\CoursAlternance\CASPRATIQUE\py-traducteur\api_traducteur\src>

ai mis sur le port 8083 a cause de conflits donc , et jai donc modifié dans parametres.py en consequence !
 http://127.0.0.1:8083/docs

appli commande : PS C:\Users\User\Downloads\CoursAlternance\CASPRATIQUE\py-traducteur\web_traducteur\src> streamlit run app.py

http://localhost:8501/

DEUX venv differents !