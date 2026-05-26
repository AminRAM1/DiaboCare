import json
from datetime import date
from LLM import analyser_etat
from react import agent_react


print("DiaboCare: 1- Tournée quotidienne ")
print("DiaboCare: 2- Urgent patient ")
today= str(date.today())
choix =input("votre choix:")

if(choix=="1"):
    with open("Patients.json","r",encoding="utf-8") as f:
        patients=json.load(f)

    for patient in patients:
        print(f"{50*'='}")
        print(f"DiaboCare: Le patient {patient['Nom']}")
        print(f"{50*'='}")
        etat=input("DiaboCare: comment vous-sentez aujourd'hui ?")
        agent_react(patient,etat)

elif(choix=="2"):
    with open("Patients.json","r",encoding="utf-8") as f:
        patients=json.load(f) 
    etat=input("DiaboCare: comment vous sentez-vous?\n")
    nom_patient=input("DiaboCare: quel est votre nom?\n")
    patient_trouve=None
    for patient in patients:
        if(patient["Nom"]==nom_patient):
            patient_trouve=patient
            break

    if(patient_trouve==None):
        print("DiaboCare: patient non trouve\n")

    else:
        agent_react(patient_trouve,etat)    
            