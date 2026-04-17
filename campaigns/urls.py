from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('campanas/', views.campaign_list, name='campaign_list'),
    path('campanas/categoria/<slug:slug>/', views.campaigns_by_category, name='campaigns_by_category'),
    path('campanas/<int:pk>/', views.campaign_detail, name='campaign_detail'),
    path('campanas/<int:pk>/donar/', views.donate, name='donate'),
    path('mis-donaciones/', views.my_donations, name='my_donations'),
]
