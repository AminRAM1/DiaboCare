import json 
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
    patient["Glycemie"]=Glycemie
    patient["Medicaments_pris"]=True if Medicament=="oui" else False 
    patient["Etat"]=etat
    with open("patients.json","w",encoding="utf-8") as f:
        json.dump(patients,f, ensure_ascii=False, indent=4)
    print("✅ Données sauvegardées !")    
