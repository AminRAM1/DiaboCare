from mistralai import Mistral
from config import API_KEY

client=Mistral(api_key=API_KEY)
def analyser_etat(etat_patient):
    
    reponse = client.chat.complete(
        model="open-mistral-7b",
        messages=[
            {
                "role": "system",
                "content": """Tu es un assistant médical.
                Analyse le message du patient, qui peut être écrit dans n'importe quelle langue.

                Détecte s'il souffre de :

                HYPERGLYCEMIE si il mentionne (dans n'importe quelle langue) :
                - fatigue intense / intense fatigue / إرهاق شديد / fatiga intensa
                - soif excessive / excessive thirst / عطش شديد / sed excesiva
                - urines fréquentes / frequent urination / كثرة التبول / micción frecuente
                - vision floue / blurry vision / رؤية ضبابية / visión borrosa
                - maux de tête / headache / headaches / صداع / dolor de cabeza
                - bouche sèche / dry mouth / جفاف الفم / boca seca

                HYPOGLYCEMIE si il mentionne (dans n'importe quelle langue) :
                - vertiges / dizziness / دوار / mareos
                - tremblements / trembling / shaking / رعشة / temblores
                - sueurs froides / cold sweats / تعرق بارد / sudores fríos
                - palpitations / heart racing / خفقان / palpitaciones
                - confusion / confusion / ارتباك / confusión
                - faiblesse soudaine / sudden weakness / ضعف مفاجئ / debilidad repentina

                Réponds UNIQUEMENT avec un de ces mots (toujours en français) :
                - HYPERGLYCEMIE SUSPECTÉE
                - HYPOGLYCEMIE SUSPECTÉE
                - ETAT NORMAL
                - IMPOSSIBLE À DÉTERMINER

                Ne donne jamais de conseil médical direct."""
            },
            {
                "role": "user",
                "content": etat_patient
            }
        ]
    )
    return reponse.choices[0].message.content

def verifier_etat(etat_patient):
    
    reponse = client.chat.complete(
        model="open-mistral-7b",
        messages=[
            {
                "role": "system",
                "content": """Tu es un assistant médical.
                Analyse si le message du patient décrit un état de santé compréhensible.
                Le message peut être écrit dans n'importe quelle langue.

                Réponds UNIQUEMENT avec :
                - COMPREHENSIBLE si le message décrit un état de santé réel, dans n'importe quelle langue
                - AUCUN SENS si le message est incompréhensible, aléatoire ou ne décrit pas un état de santé

                Exemples COMPREHENSIBLE : "je me sens bien", "I feel dizzy", "أشعر بالتعب", "me siento mal"
                Exemples AUCUN SENS : "jhsdkjhsd", "123456", "bonjour le monde"
                """
            },
            {
                "role": "user",
                "content": etat_patient
            }
        ]
    )
    return reponse.choices[0].message.content

def traduire_paroles(agent_paroles, langue):
    
    import json
    
    reponse = client.chat.complete(
        model="open-mistral-7b",
        messages=[
            {
                "role": "system",
                "content": f"""Tu es un traducteur professionnel.
                Tu vas recevoir un dictionnaire JSON contenant des phrases en français.
                Traduis TOUTES les valeurs de ce dictionnaire en {langue}.
                Retourne UNIQUEMENT le dictionnaire JSON traduit, sans aucun texte supplémentaire.
                Les clés du dictionnaire ne doivent pas changer, seulement les valeurs."""
            },
            {
                "role": "user",
                "content": json.dumps(agent_paroles, ensure_ascii=False)
            }
        ]
    )
    
    resultat = reponse.choices[0].message.content
    resultat = resultat.strip()
    resultat = resultat.replace("```json", "").replace("```", "").strip()
    return json.loads(resultat)