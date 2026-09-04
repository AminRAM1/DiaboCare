#  DiaboCare Agent - Version Web

Agent IA autonome pour le suivi automatisé des patients diabétiques.

## Description
DiaboCare est un système intelligent qui assure le suivi quotidien des patients diabétiques via une interface web. Il contacte les patients proactivement, collecte leurs données glycémiques, détecte les anomalies et alerte les médecins en cas d'urgence.
Pour plus d'informations, vous pouvez consulter le fichier rapport DiaboCare.
##  Vidéo démonstrative:


https://github.com/user-attachments/assets/b9747682-fc3a-46ec-a778-75befcce2ee0


##  Comment lancer le projet

### 1. Installer les dépendances
```bash
pip install flask mistralai apscheduler
```

### 2. Configurer config.py
Créez un fichier `config.py` et remplissez les informations suivantes :
```python
API_KEY = "ta_cle_api_mistral"
mon_email = "ton_email@gmail.com"
code_compte = "ton_mot_de_passe_app_gmail"
```

- **API_KEY** : La clé API utilisée pour communiquer avec le modèle de langage Mistral (open-mistral-7b). Créez un compte sur https://console.mistral.ai et générez une clé API.
- **mon_email** : L'adresse Gmail utilisée par l'agent DiaboCare pour envoyer les alertes et les liens quotidiens aux patients et aux médecins.
- **code_compte** : Le mot de passe d'application Gmail (différent de votre mot de passe habituel). Créez-en un sur https://myaccount.google.com/apppasswords.

### 3. Configurer Patients.json
Le fichier `Patients.json` est la base de données qui contient tous les patients du système. Pour chaque patient, modifiez le champ `Email_med` en y mettant l'adresse email du médecin responsable — c'est cette adresse qui recevra toutes les alertes générées par l'agent DiaboCare.

### 4. Lancer le serveur
```bash
python dashboard.py
```
DiaboCare est maintenant actif et attend des accès via les liens ci-dessous :

### 4. Accéder aux interfaces
- **Interface patient (urgence)** → http://localhost:5000/PatientsInterface/Modeurgent
- **Interface patient (quotidien)** → http://localhost:5000/MedecinInterface
- **Interface médecin** → http://localhost:5000/MedecinInterface

##  Technologies utilisées
- Python
- Flask
- Mistral AI (LLM)
- HTML/CSS/JavaScript
- JSON (Base de données)
- APScheduler (emails quotidiens)

##  Auteurs
- Mohamed Amine GOUALY

##  Encadrant
- Dr Mohamed KAyyali 
