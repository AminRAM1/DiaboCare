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
                Analyse le message du patient et détecte s'il souffre de :
                
                HYPERGLYCEMIE si il mentionne : fatigue intense, soif excessive, 
                urines fréquentes, vision floue, maux de tête, bouche sèche.
                
                HYPOGLYCEMIE si il mentionne : vertiges, tremblements, 
                sueurs froides, palpitations, confusion, faiblesse soudaine.
                
                Réponds UNIQUEMENT avec un de ces mots :
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