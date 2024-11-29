from transformers import pipeline
from config.parametres import VERSIONS
from model.prompt import Prompt
import os

# Rediriger le cache
os.environ["HF_HOME"] = "C:\\Users\\User\\Documents\\huggingface_cache"

def traduire(prompt: Prompt):
    if prompt.version == VERSIONS[0]:  # fr -> en
        translator = pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en")
    elif prompt.version == VERSIONS[1]:  # en -> fr
        translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr")
    else:
        raise ValueError(f"Version de traduction inconnue : {prompt.version}")

    # Traduire le texte
    prompt.traduction = translator(prompt.atraduire)
    return prompt
