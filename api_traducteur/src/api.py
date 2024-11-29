from fastapi import FastAPI
import uvicorn
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from config.parametres import VERSIONS
from model.nlp import traduire
from model.prompt import Prompt
from dto.service_traducteur import Service_Traducteur as st
from model.utilisateur import Utilisateur
import logging

# Configurer le logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

tags =[
       {
         "name":"index",
         "description":"Index"     
       },
     {
          "name":"traduction",
          "description":"Traduction"
     },
     {
          "name":"authentification",
          "description":"authentification"
     }
]

app = FastAPI(
     title="Appli de traduction",
     description="API de traudction",
     version="1.0.0",
     openapi_tags = tags
)

@app.get("/versions", tags=["index"])
def versions():
        return VERSIONS



@app.post("/traductions", tags=["traduction"])
def traducteur(prompt: Prompt):
    try:
        logger.debug(f"Requête reçue pour /traductions avec les données : {prompt}")
        
        # Vérifier que la version est reconnue
        if prompt.version not in VERSIONS:
            raise HTTPException(status_code=400, detail=f"Version inconnue : {prompt.version}")
        
        # Processus de traduction
        traduire(prompt)
        logger.info(f"Texte traduit avec succès : {prompt.traduction}")

        # Vérifier et convertir prompt.traduction si nécessaire
        if isinstance(prompt.traduction, list):
            prompt.traduction = ", ".join([item.get('translation_text', '') for item in prompt.traduction])
            logger.debug(f"Traduction convertie en texte : {prompt.traduction}")

        # Sauvegarde dans la base de données
        logger.debug("Tentative de sauvegarde du prompt dans la base.")
        st.sauvegarder_prompt(prompt)
        logger.info("Prompt sauvegardé avec succès.")

        return JSONResponse(content={"traduction": prompt.traduction}, status_code=200)
    except Exception as e:
        logger.error(f"Erreur dans l'endpoint /traductions : {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")







@app.get("/traductions/auteur/{id}", tags=["traduction"])
def versions_par_auteur(id:int):
       return st.lister_prompts(id)

@app.post("/login", tags=["authentification"])
def authentifier(utilisateur:Utilisateur):
       st.verifier_login(utilisateur)
       return {"authentifié" : utilisateur.authentifie, "id":utilisateur.id}

if __name__ == "__main__" :
    uvicorn.run(app, host="0.0.0.0", port=8083)