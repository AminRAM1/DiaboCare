from mistralai import Mistral
from Tools import demander_glycemie,demander_medicament,alerter_medecin,envoyer_conseil,sauvegarder
import json
from LLM import analyser_etat
import time
import config 

client= Mistral(api_key=config.API_KEY)

outils_disponibles = """
- demander_glycemie : demande la glycémie au patient
- demander_medicament : demande si le patient a pris ses médicaments
- alerter_medecin : envoie une alerte au médecin
- envoyer_conseil : envoie un conseil au patient
- sauvegarder : sauvegarde les données dans le JSON
- fin : mission accomplie, arrêter
"""
def appeler_LLM(historique):
    time.sleep(1)
    reponse = client.chat.complete(
        model="open-mistral-7b",
        messages=historique
    )
    return reponse.choices[0].message.content

def execute_action(action,patient,contexte):
    
    if action == "demander_glycemie":
        glycemie = demander_glycemie(patient)
        contexte["glycemie"]= glycemie
        return f"glycemie recuperee:{glycemie} g/L"

    elif action == "demander_medicament":
        medicament=demander_medicament(patient)
        contexte["medicament"]=medicament
        return f"medicament pris {medicament}" 

    elif action == "alerter_medecin":
        message=f"le glycemie de {patient['Nom']} est {contexte.get('glycemie', 'inconnue')} g/L"
        medecin= patient["Medecin"]
        return alerter_medecin(medecin,message)
    
    elif action == "envoyer_conseil":
        
        if contexte.get("glycemie", 1.5) > 2.5:
            conseil = "Diaboare: Évitez les sucres rapides, buvez beaucoup d'eau."
        
        elif contexte.get("glycemie", 1.5) < 0.7:
            conseil = "Diabocare: Mangez quelque chose de sucré immédiatement."
        
        else:
            conseil = "DiaboCare: Votre glycémie est stable, continuez votre traitement."
        envoyer_conseil(conseil)
        return "Conseil envoyé"

    elif action == "sauvegarder":
        nom_patient,GLYCEMIE,ETAT,MEDICAMENT = patient["Nom"],contexte.get("glycemie", 0),contexte.get("etat", ""),contexte.get("medicament", "")
        
        if(0.7 <= GLYCEMIE <= 2.5):
            prediction=analyser_etat(ETAT)
            if(prediction == "HYPERGLYCEMIE SUSPECTÉE" or prediction == "HYPoGLYCEMIE SUSPECTÉE"):
                ETAT=f"{nom_patient}:"+ ETAT +f" DiaboCare:{prediction}"
            
        sauvegarder(nom_patient,
            GLYCEMIE,
            ETAT,
            MEDICAMENT)
        return "Données sauvegardées"
    
    elif action == "fin":
        return "fin"
    
    return "Action inconnue"
     


def agent_react(patient,etat):

    contexte= {"etat":etat}
    
    historique= [
           
           {
    "role": "system",
    "content": f"""Tu es un agent médical autonome ReAct.
            
PATIENT : {patient['Nom']}
MEDECIN : {patient['Medecin']}
ETAT DÉCRIT : {etat}

RÈGLES MÉDICALES :
- Glycémie > 2.5 g/L = HYPERGLYCEMIE → alerter_medecin puis envoyer_conseil
- Glycémie < 0.7 g/L = HYPOGLYCEMIE → alerter_medecin puis envoyer_conseil
- 0.7 <= Glycémie <= 2.5 = NORMAL → envoyer_conseil

ORDRE DES ACTIONS OBLIGATOIRE :
1. demander_glycemie
2. demander_medicament
3. alerter_medecin (si glycémie critique)
4. envoyer_conseil (TOUJOURS, même après une alerte)
5. sauvegarder
6. fin

OUTILS DISPONIBLES :
{outils_disponibles}

TU DOIS répondre UNIQUEMENT avec le nom d'un outil à chaque fois.
Exemple : demander_glycemie
Ne jamais sauter l'étape envoyer_conseil.
Ne jamais donner de conseil médical direct.
Réfléchis étape par étape."""
},
{
    "role": "user",
    "content": "Commence le suivi du patient. Quel est ton premier outil ?"
}
    ]
    
    for i in range(10):
        
        action=appeler_LLM(historique).strip().lower()
        print(f"Tought: LLM a choisi :{action}")
        resultat=execute_action(action,patient,contexte)
        
        if(resultat == "fin" or action =="fin"):
            print(f"mession complete pour le patient {patient['Nom']}")
            break

        historique.append({"role": "assistant", "content": action})
        historique.append({"role": "user", "content": f"Résultat : {resultat}. Quel est le prochain outil ?"})
        

        


    
    


