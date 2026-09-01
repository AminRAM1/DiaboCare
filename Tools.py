import json
from datetime import date
import smtplib
from email.mime.text import MIMEText
from config import mon_email,code_compte


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
    print(f"DiaboCare: Alerte envoyée au médecin {nom_medecin} dans son email.")
    return "Alerte envoyée"

def envoyer_conseil(conseil):
    print(f"{conseil}")
    return "Conseil envoyé"

def sauvegarder(nom_patient, glycemie, etat, medicament,cmp,derniere_session):
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
            patient["derniere_session"]=derniere_session
            break
    
    with open("Patients.json", "w", encoding="utf-8") as f:
        json.dump(patients, f, ensure_ascii=False, indent=4)
    
    return "Données sauvegardées"

def envoye_email(medicin_email,message_to_med,nom_patient):
    
    try:
        message=MIMEText(message_to_med)
        message["Subject"]=f"alert au medecin pour le patient {nom_patient} "
        message["From"]=mon_email
        message["To"]=medicin_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as serveur:
            serveur.login(mon_email, code_compte)
            serveur.send_message(message)
    
    except Exception as e:
        print("erreur d'envoye l'email")
    
    return "message_envoyé"

