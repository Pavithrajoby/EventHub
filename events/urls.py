from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('event/create/', views.event_create, name='event_create'),
    path('event/<slug:slug>/', views.event_detail, name='event_detail'),
    path('event/<slug:slug>/edit/', views.event_edit, name='event_edit'),
    path('event/<slug:slug>/delete/', views.event_delete, name='event_delete'),
    path('event/<slug:slug>/register/', views.register_event, name='register_event'),
    path('event/<slug:slug>/cancel/', views.cancel_registration, name='cancel_registration'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('verify-ticket/', views.verify_ticket, name='verify_ticket'),
    path('qr-scanner/', views.qr_scanner, name='qr_scanner'),
    path('check-ticket-status/', views.check_ticket_status, name='check_ticket_status'),
]
