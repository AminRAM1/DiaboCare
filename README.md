#  DiaboCare Agent — Version Web

Agent IA autonome pour le suivi automatisé des patients diabétiques.

## Description
DiaboCare est un système intelligent qui assure le suivi quotidien des patients diabétiques via une interface web. Il contacte les patients proactivement, collecte leurs données glycémiques, détecte les anomalies et alerte les médecins en cas d'urgence.

##  Comment lancer le projet

### 1. Installer les dépendances
```bash
pip install flask mistralai apscheduler
```

### 2. Configurer config.py
```python
API_KEY = "ta_cle_api_mistral"
mon_email = "ton_email@gmail.com"
code_compte = "ton_mot_de_passe_app_gmail"
```

### 3. Lancer le serveur
```bash
python dashboard.py
```

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
