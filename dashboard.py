from flask import Flask, render_template, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from urllib.parse import quote
from Tools import envoye_email,sauvegarder
import json
import react
from LLM import analyser_etat , verifier_etat, traduire_paroles
import time
from datetime import date
app = Flask(__name__)
twodays=None

agent_paroles={"mot_passe":"saisir votre mot de passe",
               "etat":"comment vous senter haujourd'hui?",
               "glycemie":"quelle est votre glycemie en (g/L) ?",
               "medicament":"avez-vous pris les medicament ?",
               "deja_effectue_suivi":"Vous avez déjà effectué votre suivi aujourd'hui. À demain",
               "patient_non_trouve":"Patient not found. Please try again (enter your full name with your first name first, example: Mohamed Amine Goualy).",
               "mot_passe_incorrect":"mot passe incorrect",
               "message_incomprehensible":"Votre message est incompréhensible, veuillez répéter",
               "glycemie_erreur":"Veuillez entrer un nombre valide. Ex: 1.8",
               "etat_erreur":"Veuillez entrer une réponse valide. Ex: \"oui\" ou \"non",
               "alerte_2jrs_consecutives":" Alerte envoyée au médecin, vous n'avez pas pris les medicaments pour 2 jours consecutive!",
               "alerte_hyperglycemie":"Hypoglycémie détectée ! Alerte envoyée au médecin,\n Mangez quelque chose de sucré immédiatement",
               "alerte_hypoglycemie":"Hypoglycémie détectée ! Alerte envoyée au médecin,\n Mangez quelque chose de sucré immédiatement",
               "1ere_demi_alerte_prediction":" Symptômes suspects détectés.",
               "2ere_demi_alerte_prediction":" Alerte envoyée au médecin.",
               "glycemie_normal":" Glycémie normale. Continuez votre traitement et mangez équilibré.",
               "derniere_message_urgent":"Vous avez terminé le suivi d’aujourd’hui. Vous trouverez votre historique ci-dessous. Pour commencer une nouvelle session, rafraîchissez la page.",
               "derniere_message_quotidien":"Vous avez terminé le suivi d'aujourd'hui. Vous trouverez votre historique ci-dessous.",
               "HYPERGLYCEMIE_SUSPECTÉE":"HYPERGLYCEMIE SUSPECTÉE",
               "HYPOGLYCEMIE_SUSPECTÉE":"HYPOGLYCEMIE SUSPECTÉE",
               "refraicher_page":"La session est terminée. Veuillez rafraîchir la page pour commencer une nouvelle session."
                }

les_nons=["non","la","no"]
les_oui=["oui","ah","yes"]

conversation = {
    "etape": 0,
    "mode":None,
    "motPass":None,
    "etat":None,
    "glycemie":None,
    "medicament":None,
    "patient":None,
    "parole":None
}

def envoyer_emails_quotidiens():
    with open("Patients.json","r",encoding="utf-8") as f:
        patients=json.load(f)
    for patient in patients:
        lien = f"http://localhost:5000/PatientsInterface?nom={quote(patient['Nom'])}"
        message = f"Bonjour {patient['Nom']}, veuillez effectuer votre suivi quotidien : {lien}"
        envoye_email(patient["Email_patient"],message,patient["Nom"])

scheduler = BackgroundScheduler()
scheduler.add_job(envoyer_emails_quotidiens, 'cron', hour=20, minute=46)
scheduler.start()
today=str(date.today())

@app.route("/PatientsInterface")
def patient():
    nom = request.args.get("nom", "")
    return render_template("PatientsInterface.html", nom=nom, mode="quotidien")

@app.route("/PatientsInterface/Modeurgent")
def patient_urgent():
    return render_template("PatientsInterface.html", nom="", mode="urgent")

@app.route("/MedecinInterface")
def medecin():
    with open("Patients.json", "r", encoding="utf-8") as f:
        patients = json.load(f)
    return render_template("MedecinInterface.html", patients=patients)

@app.route("/reset", methods=["POST"])
def reset():
    conversation["mode"] = None
    conversation["etape"] = None
    conversation["etat"] = None
    conversation["glycemie"] = None
    conversation["medicament"] = None
    conversation["patient"] = None
    return jsonify({"status": "ok"})


@app.route("/chat", methods=["POST"])
def chat():
    global twodays,agent_paroles
    data = request.get_json()
    message = data["message"]
    if conversation["etape"] == 0:
        if conversation["parole"] is not None:
            refraincher_page = conversation["parole"]["refraicher_page"]
        else:
            refraincher_page = agent_paroles["refraicher_page"]
        return jsonify({"reponse": refraincher_page})
    if(conversation["mode"]==None):
        conversation["mode"] = message
        conversation["etape"] = None
        conversation["etat"] = None
        conversation["glycemie"] = None
        conversation["medicament"] = None
        conversation["patient"] = None
        twodays = None
        nom = data.get("nom", "")
        if(conversation["mode"]=="urgent"):
            conversation["etape"]=1
            return jsonify({"reponse":"What is your name?"})
        elif(conversation["mode"]=="quotidien"):
            if(conversation["patient"]==None):
                with open("Patients.json","r",encoding="utf-8") as f:
                    patients=json.load(f)
                    for patient in patients:
                        if((patient["Nom"]).lower()==nom.lower()):
                            conversation["patient"]=patient
                            break
                conversation["parole"]= traduire_paroles(agent_paroles, conversation["patient"]["langue"])
            if(conversation["mode"]=="quotidien" and conversation["patient"]["derniere_session"]==today):
                        return jsonify({"reponse": conversation["parole"]["deja_effectue_suivi"]})            
            conversation["etape"]=2
            return jsonify({"reponse": conversation["parole"]["mot_passe"]})   
    else:
        with open("Patients.json","r",encoding="utf-8") as f:
            patients=json.load(f)
        for patient in patients:
            if((patient["Nom"]).lower()==(message).lower()):
                conversation["patient"]=patient
                break       
    if(conversation["mode"]=="quotidien" and conversation["patient"]["derniere_session"]==today):
        return jsonify({"reponse": conversation["parole"]["deja_effectue_suivi"]})            
    if(conversation["etape"]==1):
            patient_trouve=None
            with open("Patients.json","r",encoding="utf-8") as f:
                patients=json.load(f)
                for patient in patients:
                    if((patient["Nom"]).lower()==(message).lower()):
                        patient_trouve=patient
                        break
                if(patient_trouve==None):
                    time.sleep(1)
                    return jsonify({"reponse": agent_paroles["patient_non_trouve"]})
                else:
                    conversation["patient"]=patient_trouve
                    conversation["etape"]=2
                    conversation["parole"]= traduire_paroles(agent_paroles, patient_trouve["langue"])
                    time.sleep(1)
                    return jsonify({"reponse":conversation["parole"]["mot_passe"]})

    elif(conversation["etape"]==2):
        mot_passe=conversation["patient"]["Mot_passe"]
        if(message==mot_passe):
            conversation["etape"]=3
            return jsonify({"reponse":conversation["parole"]["etat"]})
        else:
            return jsonify({"reponse":conversation["parole"]["mot_passe_incorrect"]})
    elif(conversation["etape"]==3):
        analyse_etat= verifier_etat(message)
        if(analyse_etat=="AUCUN SENS"):
            return jsonify({"reponse":conversation["parole"]["message_incomprehensible"]})
        conversation["etat"]=message
        conversation["etape"]=4
        time.sleep(1)
        return jsonify({"reponse":conversation["parole"]["glycemie"]})
    elif(conversation["etape"]==4):
        try:
            conversation["glycemie"]=float(message)
            conversation["etape"]=5
            time.sleep(1)
            return jsonify({"reponse":conversation["parole"]["medicament"]})
        except ValueError:
            time.sleep(1)
            return jsonify({"reponse":conversation["parole"]["glycemie_erreur"]})
    elif (conversation["etape"]==5):
        message_lower = message.lower()
        if(message_lower not in (les_nons+les_oui)):
            return jsonify({"reponse":conversation["parole"]["etat_erreur"]})
        glycemie=conversation["glycemie"]
        patient=conversation["patient"]
        etat=conversation["etat"]
        mode= conversation["mode"]
        if(message_lower in les_nons):
            message="No"
        else:
            message="Yes"
        if(message_lower in les_nons and mode=="quotidien"):
            patient["Compteur_med"]+=1
            if(patient["Compteur_med"])==2:
                patient["Compteur_med"]=0
                twodays=conversation["parole"]["alerte_2jrs_consecutives"]
                envoye_email(patient["Email_med"],f"le patient n'a pas pris les medicament pour 2j consecutives ",patient["Nom"])
        if(glycemie>2.5):
            reponse=conversation["parole"]["alerte_hyperglycemie"]
            envoye_email(patient["Email_med"],f"Hyperglycemie détectée : {glycemie} g/L",patient["Nom"])
        elif(glycemie<0.7):
            reponse=conversation["parole"]["alerte_hypoglycemie"]
            envoye_email(patient["Email_med"],f"Hypoglycemie détectée : {glycemie} g/L",patient["Nom"])
        else:
            prediction=analyser_etat(etat)
            if prediction == "HYPERGLYCEMIE SUSPECTÉE" or prediction == "HYPOGLYCEMIE SUSPECTÉE":
                if(prediction=="HYPOGLYCEMIE_SUSPECTÉE"):
                    reponse = f" {conversation['parole']['1ere_demi_alerte_prediction']} ({conversation['parole']['HYPOGLYCEMIE_SUSPECTÉE']}).{conversation['parole']['2ere_demi_alerte_prediction']}."
                else:
                    reponse = f" {conversation['parole']['1ere_demi_alerte_prediction']} ({conversation['parole']['HYPERGLYCEMIE_SUSPECTÉE']}).{conversation['parole']['2ere_demi_alerte_prediction']}."
                envoye_email(patient["Email_med"], f"Symptômes suspects : {prediction}", patient["Nom"])
            else:
                reponse = conversation["parole"]["glycemie_normal"]
        dernier_session=today
        dernier_message_urgent=conversation["parole"]["derniere_message_urgent"]
        dernier_message_quotidien=conversation["parole"]["derniere_message_quotidien"]
        sauvegarder(patient["Nom"], glycemie, etat, message,patient["Compteur_med"],dernier_session)
        refraincher_page = conversation["parole"]["refraicher_page"]
        with open("Patients.json","r",encoding="utf-8") as f:
                    patients=json.load(f)
                    for p in patients:
                        if(p["Nom"]==conversation["patient"]["Nom"]):
                            break
                    historique=p["Historique"]
        conversation["etape"] = 0
        conversation["etat"] = None
        conversation["glycemie"] = None
        conversation["medicament"] = None
        conversation["parole"]=None
        time.sleep(1)
        if(conversation["mode"]=="urgent"):
            return jsonify({"reponse": reponse,
                        "historique":historique,
                        "twodays":twodays,
                        "derniere_message":dernier_message_urgent})
        else:
            return jsonify({"reponse": reponse,
                        "historique":historique,
                        "twodays":twodays,
                        "derniere_message":dernier_message_quotidien,
                        "qtd":True}) 
    



        
    

if __name__ == "__main__":
    app.run(debug=True)