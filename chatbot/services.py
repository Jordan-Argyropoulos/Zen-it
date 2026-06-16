import openai
from django.conf import settings

class AIChatbot:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.model = "gpt-3.5-turbo"
    
    def diagnose_issue(self, user_message, context=None):
        """Analyse le problème et propose des solutions"""
        
        system_prompt = """Tu es un assistant technique expert en informatique pour Zen IT.
        Ton rôle est de :
        1. Analyser le problème décrit par l'utilisateur
        2. Proposer des solutions simples de dépannage
        3. Si le problème persiste, suggérer de créer un ticket technique
        
        Catégories de problèmes : Réseau, Matériel, Logiciel, Compte, Autre
        Priorités : Basse, Moyenne, Haute, Urgente"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        if context:
            messages.append({"role": "assistant", "content": context})
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            return self._parse_response(response.choices[0].message.content)
        except Exception as e:
            print(f"Erreur OpenAI: {e}")
            return self._fallback_response()
    
    def categorize_ticket(self, description):
        """Catégorise automatiquement le ticket"""
        
        prompt = f"""Catégorise ce problème informatique en une de ces catégories :
        - NETWORK (problèmes de connexion, wifi, internet)
        - HARDWARE (problèmes matériels, périphériques)
        - SOFTWARE (problèmes logiciels, bugs)
        - ACCOUNT (problèmes de compte, mot de passe)
        - OTHER (autre)
        
        Problème : {description}
        
        Réponds uniquement avec la catégorie (NETWORK, HARDWARE, SOFTWARE, ACCOUNT, OTHER)."""
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=10
            )
            
            return response.choices[0].message.content.strip()
        except:
            return "OTHER"
    
    def determine_priority(self, description):
        """Détermine la priorité du ticket"""
        
        prompt = f"""Détermine la priorité de ce problème informatique :
        - LOW : Problème mineur, pas urgent
        - MEDIUM : Problème impactant mais contournable
        - HIGH : Problème important nécessitant intervention rapide
        - URGENT : Problème critique (système down, perte de données)
        
        Problème : {description}
        
        Réponds uniquement avec la priorité (LOW, MEDIUM, HIGH, URGENT)."""
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=10
            )
            
            return response.choices[0].message.content.strip()
        except:
            return "MEDIUM"
    
    def _parse_response(self, response):
        """Parse la réponse de l'IA"""
        # Version simplifiée - à adapter selon vos besoins
        return {
            'diagnostic': response,
            'can_resolve': 'solution' in response.lower() or 'résolu' in response.lower(),
            'suggested_solution': response if 'solution' in response.lower() else None
        }
    
    def _fallback_response(self):
        """Réponse de secours si l'IA échoue"""
        return {
            'diagnostic': "Je ne peux pas analyser votre problème pour le moment. Un ticket va être créé pour qu'un technicien vous assiste.",
            'can_resolve': False,
            'suggested_solution': None
        }
