from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Ticket, TicketMessage
from .serializers import TicketSerializer, TicketMessageSerializer
from chatbot.services import AIChatbot

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type in ['TECH', 'ADMIN']:
            return Ticket.objects.all()
        return Ticket.objects.filter(created_by=user)
    
    def perform_create(self, serializer):
        ticket = serializer.save(created_by=self.request.user)
        
        # Analyse IA du ticket
        ai = AIChatbot()
        category = ai.categorize_ticket(ticket.description)
        priority = ai.determine_priority(ticket.description)
        
        ticket.category = category
        ticket.priority = priority
        ticket.status = 'IA_ANALYZING'
        ticket.save()
        
        # Lancer l'analyse asynchrone (à implémenter avec Celery si nécessaire)
        self._analyze_ticket(ticket)
    
    def _analyze_ticket(self, ticket):
        """Analyse le ticket avec l'IA et crée un message de diagnostic"""
        ai = AIChatbot()
        diagnosis = ai.diagnose_issue(ticket.description)
        
        # Créer un message IA avec le diagnostic
        TicketMessage.objects.create(
            ticket=ticket,
            content=f"🤖 Diagnostic IA : {diagnosis['diagnostic']}\n\n"
                   f"Priorité détectée : {ticket.get_priority_display()}\n"
                   f"Catégorie : {ticket.get_category_display()}",
            is_ai_message=True
        )
        
        # Mettre à jour le statut
        if diagnosis['can_resolve']:
            ticket.status = 'OPEN'
        else:
            ticket.status = 'OPEN'
            # Ajouter message pour technicien
            TicketMessage.objects.create(
                ticket=ticket,
                content="L'IA n'a pas pu résoudre automatiquement ce problème. "
                       "Un technicien va prendre en charge votre ticket.",
                is_ai_message=True
            )
        
        ticket.save()
    
    @action(detail=True, methods=['post'])
    def add_message(self, request, pk=None):
        ticket = self.get_object()
        serializer = TicketMessageSerializer(data=request.data)
        
        if serializer.is_valid():
            message = serializer.save(
                ticket=ticket,
                sender=request.user,
                is_ai_message=False
            )
            
            # Si c'est un technicien qui répond, analyser avec l'IA pour suggérer
            if request.user.user_type in ['TECH', 'ADMIN']:
                ai = AIChatbot()
                suggestion = ai.diagnose_issue(request.data['content'], 
                                               context=ticket.description)
                if suggestion['suggested_solution']:
                    TicketMessage.objects.create(
                        ticket=ticket,
                        content=f"💡 Suggestion IA : {suggestion['suggested_solution']}",
                        is_ai_message=True
                    )
            
            return Response(TicketMessageSerializer(message).data, 
                          status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        ticket = self.get_object()
        
        if request.user.user_type not in ['TECH', 'ADMIN']:
            return Response(
                {'error': 'Seuls les techniciens peuvent résoudre un ticket'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        ticket.status = 'RESOLVED'
        ticket.resolved_at = timezone.now()
        ticket.save()
        
        return Response({'status': 'Ticket résolu avec succès'})
