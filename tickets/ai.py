import os, json

MOCK_MODE = not os.getenv("AZURE_OPENAI_KEY")

def diagnose(text: str) -> dict:
    """
    Retourne obligatoirement:
    {
      "response": "conseil à l'utilisateur",
      "needs_technician": true/false,
      "category": "hardware|software|network|email|other",
      "priority": "low|medium|high|urgent"
    }
    """
    if MOCK_MODE:
        # Simulation intelligente basée sur mots-clés
        txt = text.lower()
        cat = "other"
        if any(x in txt for x in ["écran", "noir", "affichage", "gpu", "ordinateur ne démarre"]): cat = "hardware"
        elif any(x in txt for x in ["wifi", "internet", "connexion", "réseau"]): cat = "network"
        elif any(x in txt for x in ["logiciel", "bug", "excel", "mot de passe oublié"]): cat = "software"
        
        pri = "medium"
        if any(x in txt for x in ["bloqué", "impossible", "urgent", "péril"]): pri = "high"
        
        return {
            "response": "Avez-vous essayé de redémarrer l'appareil ou de vérifier les câbles de connexion ? Si le problème persiste, un technicien pourra intervenir.",
            "needs_technician": True,
            "category": cat,
            "priority": pri
        }

    # --- Vrai appel Azure OpenAI ---
    try:
        from openai import AzureOpenAI
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version="2024-02-01",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        
        system = """Tu es un assistant helpdesk N1. L'utilisateur décrit un problème IT.
Réponds UNIQUEMENT au format JSON suivant sans autre texte:
{"response":"conseil premier niveau","needs_technician":true/false,"category":"hardware|software|network|email|other","priority":"low|medium|high|urgent"}"""
        
        resp = client.chat.completions.create(
            model="gpt-4o-mini",  # ou le nom de ton deployment Azure
            messages=[{"role":"system","content":system},{"role":"user","content":text}],
            response_format={"type":"json_object"}
        )
        return json.loads(resp.choices[0].message.content)
    except Exception as e:
        
        return {"response":"Un technicien va examiner votre cas.","needs_technician":True,"category":"other","priority":"medium"}
