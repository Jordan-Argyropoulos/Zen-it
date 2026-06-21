from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from .models import Ticket
from .ai import diagnose
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def diagnose_view(request):
    if request.method == 'POST':
        problem = request.POST.get('problem','').strip()
        if not problem:
            return render(request, 'diagnose.html', {'error':'Décrivez votre problème.'})
        
        # Simule "l'IA de première ligne"
        ai_result = diagnose(problem)
        request.session['diagnosis'] = ai_result
        request.session['problem_text'] = problem
        return redirect('diagnose_result')
    return render(request, 'diagnose.html')

@login_required
def diagnose_result(request):
    d = request.session.get('diagnosis')
    if not d: return redirect('diagnose')
    return render(request, 'diagnose_result.html', {'ai': d})

@login_required
def ticket_create(request):
    """Appelé quand l'utilisateur clique sur 'Non, contacter un technicien'"""
    d = request.session.get('diagnosis')
    p = request.session.get('problem_text')
    if not d or not p: return redirect('diagnose')
    
    with transaction.atomic():
        t = Ticket.objects.create(
            user=request.user,
            title=(p[:60] + "...") if len(p)>60 else p,
            description=p,
            category=d.get('category','other'),
            priority=d.get('priority','medium'),
            ai_first_response=d.get('response','')
        )
    # Cleanup session
    request.session.pop('diagnosis',None)
    request.session.pop('problem_text',None)
    return redirect('ticket_detail', ticket_id=t.id)

@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user) if not request.user.is_technician else get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'ticket_detail.html', {'ticket': ticket})

@login_required
def dashboard(request):
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'tickets': tickets})

@staff_member_required  # ou décorateur perso vérifiant is_technician
def tech_dashboard(request):
    # Technicien voit les tickets New/Open non assignés ou assignés à lui
    tickets = Ticket.objects.filter(status__in=['new','open']).order_by('-priority','-created_at')
    return render(request, 'tech/dashboard.html', {'tickets': tickets})

@staff_member_required
def take_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket.technician = request.user
    ticket.status = 'open'
    ticket.save()
    return redirect('tech_dashboard')
