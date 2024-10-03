from django.urls import path
from . import views
from .views import index

urlpatterns = [
    path('index/', index, name='index'), # Page index
    path('', views.home, name='home'),  # Route pour la page d'accueil
    path('shop/', views.shop, name='shop'),  # Route pour la page de boutique
    path('product-details/', views.product_details, name='product_details'),  # Route pour les détails du produit
    path('contact/', views.contact, name='contact'),  # Route pour la page de contact
    path('sign-in/', views.sign_in, name='sign_in'),  # Route pour la page de connexion
]