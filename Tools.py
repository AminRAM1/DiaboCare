import json
from datetime import date

today=str(date.today())
def demander_glycemie(nom_patient):
    while True:
        try:
            Glycemie=float(input("DiaboCAre: quelle est votre glycemie aujourd'hui?"))
            return Glycemie
        except ValueError:
            print("DiaboCare: entrer un nom valide (ex 1.8)")

def demander_medicament(nom_patient):
    Medicament= input("DiaboCare: vous avez pris vous medicaments?")
    return Medicament.lower()

def alerter_medecin(nom_medecin,message):
    print(f"DiaboCare: ALERTE MÉDECIN ({nom_medecin}): {message}  ")
    return "Alerte envoyée"

def envoyer_conseil(conseil):
    print(f"{conseil}")
    return "Conseil envoyé"

def sauvegarder(nom_patient, glycemie, etat, medicament,cmp):
    with open("Patients.json", "r", encoding="utf-8") as f:
        patients = json.load(f)
    
    for patient in patients:
        if patient["Nom"] == nom_patient:
            entree = {
                "date": today,
                "Glycemie": glycemie,
                "Etat": etat,
                "Medicament_pris": medicament
            }
            patient["Historique"].append(entree)
            patient["Compteur_med"]=cmp
            break
    
    with open("Patients.json", "w", encoding="utf-8") as f:
        json.dump(patients, f, ensure_ascii=False, indent=4)
    
    return "Données sauvegardées"


