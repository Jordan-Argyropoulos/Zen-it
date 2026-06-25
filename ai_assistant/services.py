import openai
from django.conf import settings

class AIChatbot:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.model = "gpt-3.5-turbo"
    
    def categorize_ticket(self, description):
        """Catégorise automatiquement le ticket avec l'IA"""
        
        # Si pas de clé API, utiliser une catégorisation simple
        if not settings.OPENAI_API_KEY:
            return self._simple_categorize(description)
        
        prompt = f"""En tant qu'expert en support informatique, catégorise ce problème technique.
        
Catégories possibles :
- NETWORK : Problèmes de connexion, wifi, internet, réseau
- HARDWARE : Problèmes matériels, ordinateur qui ne démarre pas, écran noir, bruit anormal
- SOFTWARE : Problèmes logiciels, bugs, plantages, erreurs d'application
- ACCOUNT : Problèmes de compte, mot de passe, authentification
- OTHER : Autre problème non classable

Problème : {description}

Réponds UNIQUEMENT avec la catégorie (NETWORK, HARDWARE, SOFTWARE, ACCOUNT ou OTHER)."""
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Tu es un classificateur de tickets de support informatique. Réponds uniquement avec la catégorie."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=10
            )
            
            category = response.choices[0].message.content.strip().upper()
            valid_categories = ['NETWORK', 'HARDWARE', 'SOFTWARE', 'ACCOUNT', 'OTHER']
            
            return category if category in valid_categories else 'OTHER'
            
        except Exception as e:
            print(f"Erreur OpenAI: {e}")
            return self._simple_categorize(description)
    
    def determine_priority(self, description):
        """Détermine la priorité du ticket"""
        
        if not settings.OPENAI_API_KEY:
            return 'MEDIUM'
        
        prompt = f"""En tant qu'expert en support informatique, détermine la priorité de ce problème.

Priorités :
- URGENT : Système complètement down, perte de données, impact critique sur le business
- HIGH : Problème important bloquant le travail mais avec contournement possible
- MEDIUM : Problème impactant mais pas bloquant
- LOW : Question ou problème mineur

Problème : {description}

Réponds UNIQUEMENT avec la priorité (URGENT, HIGH, MEDIUM ou LOW)."""
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Tu es un évaluateur de priorité de tickets. Réponds uniquement avec la priorité."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=10
            )
            
            priority = response.choices[0].message.content.strip().upper()
            valid_priorities = ['URGENT', 'HIGH', 'MEDIUM', 'LOW']
            
            return priority if priority in valid_priorities else 'MEDIUM'
            
        except Exception as e:
            print(f"Erreur OpenAI: {e}")
            return 'MEDIUM'
    
    def diagnose_issue(self, description):
        """Analyse le problème et propose des solutions"""
        
        if not settings.OPENAI_API_KEY:
            return {
                'diagnostic': "Le service IA n'est pas configuré. Un technicien va prendre en charge votre ticket manuellement.",
                'can_resolve': False
            }
        
        prompt = f"""En tant qu'expert en support informatique de Zen IT, analyse ce problème technique et propose une solution.

Utilisateur : {description}

Structure ta réponse en 3 parties :
1. DIAGNOSTIC : Analyse du problème probable
2. SOLUTION : Étapes de dépannage (simples et claires)
3. CONCLUSION : Si le problème peut être résolu avec ces étapes ou si un technicien doit intervenir"""
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Tu es un assistant technique expert. Sois clair, précis et utile."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            diagnostic = response.choices[0].message.content
            
            return {
                'diagnostic': diagnostic,
                'can_resolve': 'technicien' not in diagnostic.lower() and 'intervenir' not in diagnostic.lower()
            }
            
        except Exception as e:
            print(f"Erreur OpenAI: {e}")
            return {
                'diagnostic': "Désolé, je n'ai pas pu analyser votre problème pour le moment. Un technicien va vous assister.",
                'can_resolve': False
            }
    
    def _simple_categorize(self, description):
        """Catégorisation simple sans IA"""
        desc_lower = description.lower()
        
        if any(word in desc_lower for word in ['wifi', 'internet', 'réseau', 'connexion', 'network']):
            return 'NETWORK'
        elif any(word in desc_lower for word in ['écran', 'démarre', 'bruit', 'clavier', 'souris', 'hardware']):
            return 'HARDWARE'
        elif any(word in desc_lower for word in ['logiciel', 'bug', 'erreur', 'plantage', 'software', 'application']):
            return 'SOFTWARE'
        elif any(word in desc_lower for word in ['compte', 'mot de passe', 'password', 'login', 'authentification']):
            return 'ACCOUNT'
        else:
            return 'OTHER'
