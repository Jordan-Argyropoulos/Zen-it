from django.urls import path
from . import views
urlpatterns = [
    path('diagnose/', views.diagnose_view, name='diagnose'),
    path('diagnose/result/', views.diagnose_result, name='diagnose_result'),
    path('diagnose/escalate/', views.ticket_create, name='ticket_escalate'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tickets/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('tech/', views.tech_dashboard, name='tech_dashboard'),
    path('tech/take/<int:ticket_id>/', views.take_ticket, name='take_ticket'),
]
