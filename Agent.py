import json
from datetime import date
print("1- Tournée quotidienne ")
print("2- Urgent patient ")
today= str(date.today())
choix =input("votre choix:")

if(choix=="1"):
    with open("Patients.json","r",encoding="utf-8") as f:
        patients=json.load(f)

    for patient in patients:
        Nom_patient=patient["Nom"]
        print(f"\n{'='*50}")
        print("👤 Patient",Nom_patient)
        print(f"\n{'='*50}")
        print(f"\n🤖 Agent : Bonjour {Nom_patient}, comment vous sentez-vous aujourd'hui?")
        etat = input("👤 Patient:")
        print("\n🤖 Agent: Quelle est votre glycémie aujourd'hui ? (en g/L)")
        Glycemie=float(input("👤 Patient:"))
        print("\n🤖 Agent : Avez-vous pris vos médicaments ? (oui/non)")
        Medicament=input("👤 Patient:")   
        print(f"\n🔍 Analyse en cours...")

        if(Glycemie>2.5):
            print(f"🔴 CRITIQUE : Hyperglycémie détectée !")
            print(f"⚠️  Alerte envoyée à {patient['Medecin']}")
            print(f"🤖 Agent : Évitez les sucres rapides, buvez beaucoup d'eau et reposez-vous.")

        elif(Glycemie<0.7):
            print(f"🔴 CRITIQUE : Hypoglycémie détectée !")
            print(f"⚠️  Alerte envoyée à {patient['Medecin']}")
            print(f"🤖 Agent : Mangez quelque chose de sucré immédiatement (jus, sucre...).") 
        else:
            print(f"✅ Glycémie normale")
            print(f"🤖 Agent : Très bien {Nom_patient}, continuez à suivre votre traitement et mangez équilibré.")
        
        if(Medicament=="Non" or Medicament=="non"):
            print(f"⚠️  AVERTISSEMENT : Médicament non pris !")

    #Saving Data
        entree={"date":today,"Glycemie":Glycemie,"Etat":etat,"Medicament_pris":Medicament}
        patient["Historique"].append(entree)
        with open("patients.json","w",encoding="utf-8") as f:
            json.dump(patients,f, ensure_ascii=False, indent=4)
        print("✅ Données sauvegardées !")  


elif(choix=="2"):
    with open("Patients.json","r",encoding="utf-8") as f:
        patients=json.load(f) 
    etat=input("comment vous sentez-vous?\n")
    Nom_patient=input("Quelle est votre nom:\n")
    patient_trouve=None
    for patient in patients:
        if(patient["Nom"]==Nom_patient):
            patient_trouve=patient
            break

    if(patient_trouve==None):
        print("Patient non trouvee !")

    else:
        Glycemie=float(input("Quelle est votre glycémie ?\n"))
        if(Glycemie>2.5):
            print("🔴 CRITIQUE : Hyperglycémie détectée !\n")
            print(f"⚠️  Alerte envoyée à {patient['Medecin']}\n")
            print("🤖 Agent : Restez calme, le médecin a été alerté et va vous contacter.")

        elif(Glycemie<0.7):
            print("🔴 CRITIQUE : Hypoglycémie détectée !\n")
            print(f"⚠️  Alerte envoyée à {patient['Medecin']}\n")
            print("🤖 Agent : Restez calme, le médecin a été alerté et va vous contacter.\n")
        else:
            print("✅ Glycémie normale")
            print("🤖 Agent : Votre glycémie est stable, surveillez votre état et contactez votre médecin si ça empire.")
        #sauvegarder les donnees:
        if(patient_trouve!=None):
            entree={"date":today,"Glycemie":Glycemie,"Etat":etat,"Medicament_pris":""}
            patient["Historique"].append(entree)

            with open("patients.json","w",encoding="utf-8") as f:
                json.dump(patients,f, ensure_ascii=False, indent=4)




