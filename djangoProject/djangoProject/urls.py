from django.conf import settings
from django.conf.urls.static import static
"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *
from django.contrib.auth import views as auth_views

from . import views

router = DefaultRouter()

router.register(r'games', VideoGameViewSet, basename='games')  # Pas besoin d'auth pour accéder aux produits

urlpatterns = [
    path('api/', include(router.urls)),
    path('', trending_games, name='index'),  # Page d'accueil
    path('api/register/', UserCreateView.as_view(), name='register'),

    # Auth routes
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Cart URLs (non via le router)
    path('product/<int:id>/', product_detail, name='product_detail'),
    path('shop/', shop, name='shop'),  # Page de la boutique avec recherche
    path('login/', user_login, name='login'),  # Route pour la page de connexion
    path('register/', register, name='register'),  # Route pour l'inscription
    path('auth/', auth_view, name='auth'),  # Route pour la page de connexion et d'inscription
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('order/create/', views.create_order, name='create_order'),
    path('api/users/<int:pk>/', CustomUserDetail.as_view(), name='user-detail'),
    # Routes pour le panier (CRUD)
    path('api/cart/items/', CartItemDetail.as_view(), name='cart-item-detail'),
    path('api/cart/items/<int:pk>/', CartItemDetail.as_view(), name='cart-item-detail'),

    # Routes pour le paiement
    path('create-payment-intent/', views.create_payment_intent, name='create_payment_intent'),
    path('confirm-payment/', views.confirm_payment, name='confirm_payment'),
    
    # Gestion du panier via API
    path('api/cart/', CartView.as_view(), name='cart'),
    path('api/cart/items/', CartItemView.as_view(), name='cart_items'),

    # Autres routes
    path('logout/', auth_views.LogoutView.as_view(next_page='auth'), name='logout'),
    path('add-to-cart/<int:game_id>/', add_to_cart, name='add_to_cart'),
    path('api/add-to-cart/', api_add_to_cart, name='api_add_to_cart'),
    path('api/token-auth/', obtain_auth_token, name='token-auth'),  # URL pour générer le token

    # Panier
    path('cart/update/<int:videoGame_id>/', update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:videoGame_id>/', remove_from_cart, name='remove_from_cart'),

    # Checkout et commandes
    path('checkout/', checkout, name='checkout'),
    path('success/', payment_success, name='payment_success'),
    path('cancel/', payment_cancel, name='payment_cancel'),
    path('order-history/', order_history, name='order_history'),
    path('order-details/<int:order_id>/', order_details, name='order_details'),  # Détails de commande
]

# Ajoute cette ligne pour servir les fichiers médias durant le développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
