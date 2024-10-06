from rest_framework import viewsets, generics, permissions
from .models import *
from .serializers import VideoGameSerializer, CartSerializer, CartItemSerializer, OrderSerializer

from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer
from django.shortcuts import render
from .models import VideoGame

from django.shortcuts import render
from .models import VideoGame

from rest_framework.permissions import AllowAny
from .serializers import UserSerializer


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import VideoGame, Cart, CartItem, Order, OrderItem
from .serializers import CartSerializer, OrderSerializer
from django.contrib.auth import get_user_model

import json
import stripe
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import Order, Cart  
def trending_games(request):
    # Récupérer les 5 derniers jeux vidéo
    trending_games = VideoGame.objects.all()[:5]  # Limite à 5 jeux
    return render(request, 'djangoProject/index.html', {'trending_games': trending_games})







User = get_user_model()
      
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Accessible à tout le monde        

# ViewSet for VideoGames (No authentication required)
def product_detail(request, id):
    game = get_object_or_404(VideoGame, id=id)
    return render(request, 'djangoProject/product-details.html', {'game': game})
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée qui permet uniquement à l'administrateur de modifier les jeux vidéo.
    Les autres utilisateurs peuvent seulement consulter (GET).
    """
    def has_permission(self, request, view):
        # Tout le monde peut voir les jeux (GET)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Seul l'administrateur peut faire des modifications (POST, PUT, DELETE)
        return request.user and request.user.is_staff
class VideoGameViewSet(viewsets.ModelViewSet):
    queryset = VideoGame.objects.all()
    serializer_class = VideoGameSerializer
    permission_classes = [IsAdminOrReadOnly]  # Accessible à tout le monde

# Views for Cart (Requires authentication)


# Ajouter un article au panier
@api_view(['POST'])
def add_to_cart(request):
    user = request.user
    video_game_id = request.data.get('video_game_id')
    quantity = request.data.get('quantity', 1)
    
    try:
        video_game = VideoGame.objects.get(id=video_game_id)
    except VideoGame.DoesNotExist:
        return Response({'error': 'Video game not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Récupérer ou créer le panier de l'utilisateur
    cart, created = Cart.objects.get_or_create(customuser=user)
    
    # Ajouter ou mettre à jour l'article dans le panier
    cart_item, created = CartItem.objects.get_or_create(cart=cart, videoGame=video_game)
    cart_item.quantity += int(quantity)
    cart_item.save()
    
    return Response({'message': 'Item added to cart'}, status=status.HTTP_200_OK)

# Voir le contenu du panier
@api_view(['GET'])
def view_cartapi(request):
    user = request.user
    try:
        cart = Cart.objects.get(customuser=user)
    except Cart.DoesNotExist:
        return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CartSerializer(cart)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Créer une commande à partir du panier
@api_view(['POST'])
def create_order(request):
    user = request.user
    try:
        cart = Cart.objects.get(customuser=user)
    except Cart.DoesNotExist:
        return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

    if not CartItem.objects.filter(cart=cart).exists():
        return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

    # Créer la commande
    order = Order.objects.create(customuser=user, total_price=0, status='pending')
    
    total_price = 0
    for cart_item in CartItem.objects.filter(cart=cart):
        OrderItem.objects.create(order=order, videoGame=cart_item.videoGame, quantity=cart_item.quantity)
        total_price += cart_item.videoGame.price * cart_item.quantity
    
    # Mettre à jour le prix total et vider le panier
    order.total_price = total_price
    order.save()
    cart.cartitem_set.all().delete()  # Vide le panier

    return Response({'message': 'Order created'}, status=status.HTTP_201_CREATED)


    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        cart = Cart.objects.get(user=self.request.user)
        # Calculer le total des prix dans le panier
        total_price = sum([item.game.price * item.quantity for item in cart.items.all()])
        # Créer la commande
        order = serializer.save(user=self.request.user, total_price=total_price)
        # Ajouter les items du panier à la commande
        for item in cart.items.all():
            OrderItem.objects.create(order=order, game=item.game, quantity=item.quantity)
        # Vider le panier après validation de la commande
        cart.items.all().delete()

from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm  # Assure-toi d'importer tes formulaires
from rest_framework import permissions




    

class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Lecture permise pour tout le monde
        return request.user and request.user.is_staff  # Modifications seulement pour les admins
    

from rest_framework.permissions import IsAdminUser


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # L'utilisateur doit être authentifié

    def get_permissions(self):
        # Si l'utilisateur est le superutilisateur, il peut faire toutes les actions
        if self.request.method in ['DELETE', 'PUT']:
            self.permission_classes = [IsAdminUser]  # Superuser uniquement
        return super().get_permissions()
    
from django.http import Http404

class CustomUserDetail(APIView):
    """
    Récupérer, mettre à jour ou supprimer un utilisateur.
    Un utilisateur ne peut modifier ou supprimer que son propre compte.
    Seul un superuser peut supprimer n'importe quel compte.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        # Seul le propriétaire ou un superuser peut récupérer ses informations
        if request.user == user or request.user.is_superuser:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        # Seul le propriétaire peut modifier son compte
        if request.user == user:
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "You do not have permission to edit this account."}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        # Seul le propriétaire ou un superuser peut supprimer son compte
        if request.user == user or request.user.is_superuser:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "You do not have permission to delete this account."}, status=status.HTTP_403_FORBIDDEN)





class CartDetail(APIView):
    """
    Récupérer ou mettre à jour le panier de l'utilisateur authentifié.
    Seul l'utilisateur connecté peut gérer son propre panier.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Vérifier que le panier appartient à l'utilisateur authentifié
        try:
            return Cart.objects.get(customuser=self.request.user)
        except Cart.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        cart = self.get_object()  # Récupérer le panier de l'utilisateur authentifié
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def put(self, request, format=None):
        cart = self.get_object()  # Récupérer le panier de l'utilisateur authentifié
        serializer = CartSerializer(cart, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Gérer les éléments du panier (ajouter, modifier, ou supprimer des articles)
class CartItemDetail(APIView):
    """
    Gérer les articles dans le panier de l'utilisateur (ajouter, modifier, supprimer).
    Seul l'utilisateur connecté peut gérer les articles de son propre panier.
    """
    permission_classes = [IsAuthenticated]

    def get_cart(self):
        # Créer ou récupérer le panier de l'utilisateur
        cart, created = Cart.objects.get_or_create(customuser=self.request.user)
        return cart

    def get_object(self, pk):
        # Vérifier que l'élément de panier appartient au panier de l'utilisateur authentifié
        try:
            return CartItem.objects.get(pk=pk, cart__customuser=self.request.user)
        except CartItem.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        # Créer un nouvel élément de panier pour l'utilisateur authentifié
        cart = self.get_cart()
        game_id = request.data.get('game')  # Utilisez 'game' au lieu de 'videoGame'
        quantity = request.data.get('quantity')

        try:
            video_game = VideoGame.objects.get(id=game_id)  # Utilisez 'game_id' pour la recherche
        except VideoGame.DoesNotExist:
            return Response({"detail": "Video game not found."}, status=status.HTTP_404_NOT_FOUND)

        # Ajouter un article au panier de l'utilisateur connecté
        cart_item, created = CartItem.objects.get_or_create(cart=cart, videoGame=video_game,quantity=quantity)  # Utilisez 'videoGame' ici
        cart_item.quantity = quantity  # Assignez la quantité
        cart_item.save()  # Appelez save() sans arguments

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def put(self, request, pk, format=None):
        # Mettre à jour la quantité d'un article du panier basé sur videoGame_id
        cart = self.get_cart()  # Récupérer le panier de l'utilisateur
        try:
            cart_item = CartItem.objects.get(cart=pk)  # Rechercher par videoGame_id
        except CartItem.DoesNotExist:
            return Response({"detail": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)

        # Mettre à jour la quantité
        quantity = request.data.get('quantity')
        if quantity is not None:
            cart_item.quantity = quantity
            cart_item.save()  # Sauvegarder les modifications
        else:
            return Response({"detail": "Quantity not provided."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def delete(self, request, pk, format=None):
        # Rechercher l'élément de panier à supprimer basé sur videoGame_id
        cart = self.get_cart()  # Récupérer le panier de l'utilisateur
        try:
            cart_item = CartItem.objects.get(cart=cart, videoGame_id=pk)  # Rechercher par videoGame_id
        except CartItem.DoesNotExist:
            return Response({"detail": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()  # Supprimer l'objet
        return Response(status=status.HTTP_204_NO_CONTENT)


stripe.api_key = settings.STRIPE_SECRET_KEY

def calculate_total_price(customuser):
    # Récupérer le panier de l'utilisateur
    cart = Cart.objects.get(customuser=customuser)  # Assurez-vous que l'utilisateur a un panier
    cart_items = CartItem.objects.filter(cart=cart)

    # Calculer le prix total
    total_price = sum(item.videoGame.price * item.quantity for item in cart_items)
    return total_price


@csrf_exempt
@api_view(['POST']) 
@permission_classes([IsAuthenticated])  # Ajoutez ceci pour la permission
def confirm_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            payment_intent_id = data['paymentIntentId']
            payment_method = data['paymentMethod']

            # Confirmation du PaymentIntent
            intent = stripe.PaymentIntent.confirm(
                payment_intent_id,
                payment_method=payment_method
            )

            # Créer une commande ici si le paiement a réussi
            if intent['status'] == 'succeeded':
                # Récupérer le prix total et créer la commande
                total_price = calculate_total_price(request.user)  # Récupérez le prix total
                order = Order.objects.create(
                    customuser_id=request.user.id,  # Utilisateur authentifié (ID uniquement)
                    total_price=total_price,   # Prix total calculé
                    status='completed'
                )

                # Réduire la quantité des jeux dans le panier
                cart = Cart.objects.get(customuser=request.user)  # Récupérer le panier de l'utilisateur
                cart_items = CartItem.objects.filter(cart=cart)  # Obtenir les articles du panier

                for item in cart_items:
                    game = item.videoGame  # Référence au modèle de jeu
                    if game.stock >= item.quantity:
                        game.stock -= item.quantity  # Réduire la quantité
                        game.save()  # Enregistrer les changements
                    else:
                        return JsonResponse({'error': f'Not enough quantity for game: {game.title}'}, status=400)

                # Optionnel : vider le panier après la commande
                cart_items.delete()  # Cela supprime les articles du panier

                # Créer un nouveau panier pour l'utilisateur
                new_cart = Cart.objects.create(customuser=request.user)

            return JsonResponse({'status': intent['status']})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)



@csrf_exempt
def create_payment_intent(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Récupérer les données du corps de la requête
            amount = data['amount']  # Le montant doit être en cents (ou la plus petite unité de la devise)
            currency = data.get('currency', 'usd')  # Par défaut, utilisez la devise USD si aucune autre devise n'est fournie

            # Créez le PaymentIntent avec le montant et la devise
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                payment_method_types=['card']  # Stripe propose plusieurs méthodes de paiement, ici on utilise les cartes bancaires
            )

            # Renvoyer le client secret pour le frontend
            return JsonResponse({
                'clientSecret': payment_intent['client_secret'],  # Le client secret sera utilisé sur le frontend pour finaliser le paiement
                'paymentIntentId': payment_intent['id']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)




@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Assurez-vous que l'utilisateur est authentifié
def get_orders(request):
    # Si l'utilisateur est un administrateur, il peut voir toutes les commandes
    if request.user.is_staff:
        orders = Order.objects.all()
    else:
        # Sinon, il ne voit que ses propres commandes
        orders = Order.objects.filter(customuser=request.user)
    
    # Utilisation du sérialiseur pour transformer les objets en JSON
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)











from rest_framework import viewsets, generics, permissions
from .models import *
from .serializers import VideoGameSerializer, CartSerializer, CartItemSerializer, OrderSerializer

from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from rest_framework.authtoken.views import obtain_auth_token




from django.shortcuts import render
from .models import VideoGame

from django.shortcuts import render
from .models import VideoGame

@login_required(login_url='/login/')  # Redirige vers la page de login si non authentifié
def shop(request):
    # Récupérer les filtres depuis les paramètres GET
    search_keyword = request.GET.get('searchKeyword', '')
    selected_category = request.GET.get('category', '')
    max_price = request.GET.get('price', 1000)  # Prix maximal par défaut à 1000 $

    # Commencer par récupérer tous les jeux
    games = VideoGame.objects.all()

    # Filtrer par catégorie si une catégorie est sélectionnée
    if selected_category:
        games = games.filter(category__iexact=selected_category)

    # Filtrer par mot-clé de recherche si un mot-clé est fourni
    if search_keyword:
        games = games.filter(title__icontains=search_keyword)

    # Filtrer par fourchette de prix
    games = games.filter(price__lte=max_price)

    # Obtenir toutes les catégories disponibles pour la liste déroulante
    categories = VideoGame.objects.values_list('category', flat=True).distinct()

    return render(request, 'djangoProject/shop.html', {
        'games': games,
        'categories': categories,
        'search_keyword': search_keyword,
        'selected_category': selected_category,
        'max_price': max_price
    })




def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('shop')  # Rediriger l'utilisateur après la connexion
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'djangoProject/login.html', {'form': form})


# ViewSet for VideoGames (No authentication required)
def product_detail(request, id):
    game = get_object_or_404(VideoGame, id=id)
    return render(request, 'djangoProject/product-details.html', {'game': game})
class VideoGameViewSet(viewsets.ModelViewSet):
    queryset = VideoGame.objects.all()
    serializer_class = VideoGameSerializer
    permission_classes = [permissions.AllowAny]  # Accessible à tout le monde

# Views for Cart (Requires authentication)
class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Cart.objects.get(user=self.request.user)

class CartItemView(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        cart = Cart.objects.get(user=self.request.user)
        return CartItem.objects.filter(cart=cart)

    def perform_create(self, serializer):
        cart = Cart.objects.get(user=self.request.user)
        serializer.save(cart=cart)

# ViewSet for Orders (Requires authentication)
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Récupérer le panier actuel de l'utilisateur
        cart = Cart.objects.get(user=self.request.user)

        # Calculer le total des prix dans le panier
        total_price = sum([item.game.price * item.quantity for item in cart.items.all()])

        # Créer la commande
        order = serializer.save(user=self.request.user, total_price=total_price)

        # Ajouter les items du panier à la commande
        for item in cart.items.all():
            # Créer un nouvel OrderItem pour chaque item dans le panier
            OrderItem.objects.create(
                order=order,
                videoGame=item.game,
                quantity=item.quantity
            )

        # Vider le panier après validation de la commande
        cart.items.all().delete()

        # Créer un nouveau panier pour l'utilisateur après chaque commande
        Cart.objects.create(user=self.request.user)


from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige vers la page de connexion après l'inscription
        else:
            # Si le formulaire n'est pas valide, renvoyer les erreurs au template
            return render(request, 'djangoProject/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'djangoProject/register.html', {'form': form})
def custom_logout(request):
    logout(request)
    return redirect('index')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm  # Assure-toi d'importer tes formulaires


def auth_view(request):
    if request.method == 'POST':
        # Traitement du formulaire d'inscription
        if 'signup' in request.POST:
            form_signup = CustomUserCreationForm(request.POST)
            if form_signup.is_valid():
                form_signup.save()  # Enregistre le nouvel utilisateur
                messages.success(request, 'Your account has been created successfully!')
                return redirect('auth')  # Redirige vers la même page après l'inscription
            else:
                messages.error(request, 'Please correct the errors below.')

        # Traitement du formulaire de connexion
        elif 'login' in request.POST:
            form_login = CustomAuthenticationForm(data=request.POST)
            if form_login.is_valid():
                username = form_login.cleaned_data.get('username')
                password = form_login.cleaned_data.get('password')
                user = authenticate(username=username, password=password)  # Authentifie l'utilisateur
                if user is not None:
                    login(request, user)  # Connecte l'utilisateur
                    return redirect('shop')  # Redirige vers la page shop après connexion
                else:
                    messages.error(request, 'Invalid username or password')

    # Formulaires par défaut pour l'affichage
    form_signup = CustomUserCreationForm()
    form_login = CustomAuthenticationForm()

    return render(request, 'djangoProject/auth.html', {
        'form_signup': form_signup,
        'form_login': form_login,
    })
from django.shortcuts import render, redirect, get_object_or_404
from .models import VideoGame, Cart, CartItem
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404
from .models import VideoGame, Cart, CartItem
from django.contrib.auth.decorators import login_required


@login_required
def add_to_cart(request, game_id):
    game = get_object_or_404(VideoGame, id=game_id)

    # Récupérer la quantité depuis le formulaire
    quantity = request.POST.get('quantity')

    # Vérifie si quantity est fourni, sinon par défaut à 1
    if not quantity or int(quantity) < 1:
        quantity = 1  # Définit la quantité par défaut à 1
    else:
        quantity = int(quantity)  # Convertir en entier

     # Récupérer le dernier panier de l'utilisateur
    try:
        cart = Cart.objects.filter(customuser=request.user).latest('created_at')  # Récupérer le dernier panier
    except Cart.DoesNotExist:
            return JsonResponse({'error': 'No cart found for user.'}, status=404)

    cart_items = CartItem.objects.filter(cart=cart)  # Obtenir les articles du panier)

    # Ajouter l'article au panier ou mettre à jour sa quantité
    cart_item, item_created = CartItem.objects.get_or_create(quantity=quantity,cart=cart, videoGame=game)
    cart_item.quantity = quantity  # Met à jour ou définit la quantité
    cart_item.save()


    return redirect('shop')


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import VideoGame, Cart, CartItem

@api_view(['POST'])
def api_add_to_cart(request):
    user = request.user
    game_id = request.data.get('game_id')
    quantity = request.data.get('quantity', 1)

    try:
        game = VideoGame.objects.get(id=game_id)
    except VideoGame.DoesNotExist:
        return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)

    # Créer ou récupérer le panier de l'utilisateur
    cart, created = Cart.objects.get_or_create(user=user)

    # Ajouter l'article au panier ou mettre à jour sa quantité
    cart_item, item_created = CartItem.objects.get_or_create(quantity=quantity,cart=cart, game=game)
    if not item_created:
        cart_item.quantity += int(quantity)
    else:
        cart_item.quantity = int(quantity)
    cart_item.save()

    return Response({'message': 'Item added to cart successfully'}, status=status.HTTP_200_OK)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem


@login_required
def view_cart(request):
    cart = Cart.objects.filter(customuser=request.user).first()  # Récupérer le panier de l'utilisateur
    cart_items = cart.items.all() if cart else []  # Récupérer les articles du panier
    total_price = sum(item.videoGame.price * item.quantity for item in cart_items)  # Calculer le prix total

    return render(request, 'djangoProject/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })
@login_required
def update_cart_item(request, videoGame_id):
    # Récupérer l'article de panier à partir de l'ID du jeu
    cart_item = get_object_or_404(CartItem, cart__customuser=request.user, videoGame_id=videoGame_id)

    if request.method == 'POST':
        # Mettre à jour la quantité de l'article
        new_quantity = int(request.POST.get('quantity', 1))
        cart_item.quantity = new_quantity
        cart_item.save()

    return redirect('view_cart')  # Rediriger vers la page du panier

@login_required
def remove_from_cart(request, videoGame_id):
    # Récupérer l'article de panier à partir de l'ID du jeu
    cart_item = get_object_or_404(CartItem, cart__customuser=request.user, videoGame_id=videoGame_id)

    if request.method == 'POST':
        # Supprimer l'article du panier
        cart_item.delete()

    return redirect('view_cart')  # Rediriger vers la page du panier


# views.py
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY  # Configure Stripe avec ta clé secrète


@login_required
def checkout(request):
    cart = Cart.objects.filter(customuser=request.user).first()  # Récupérer le panier de l'utilisateur
    cart_items = cart.items.all() if cart else []

    if request.method == 'POST':
        line_items = []
        total_price = 0

        for item in cart_items:
            total_price += item.videoGame.price * item.quantity
            line_items.append({
                'price_data': {
                    'currency': 'eur',  # Devise en euros
                    'product_data': {
                        'name': item.videoGame.title,
                    },
                    'unit_amount': int(item.videoGame.price * 100),  # Prix en cents
                },
                'quantity': item.quantity,
            })

        # Créer une session de paiement avec Stripe
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='http://127.0.0.1:8000/success/?session_id={CHECKOUT_SESSION_ID}',
            # Redirection avec session_id
            cancel_url='http://127.0.0.1:8000/cancel/',
        )

        # Rediriger vers la session de paiement Stripe
        return redirect(checkout_session.url, code=303)

    return render(request, 'djangoProject/cart.html', {'cart_items': cart_items})


from django.db import connection


@login_required
def payment_success(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        return redirect('index')  # Si aucune session n'est trouvée, redirige vers l'accueil

    # Récupérer les informations de la session Stripe
    checkout_session = stripe.checkout.Session.retrieve(session_id)

    # Récupérer le panier de l'utilisateur
    cart = Cart.objects.filter(customuser=request.user).first()
    cart_items = cart.items.all() if cart else []

    if checkout_session.payment_status == 'paid':  # Si le paiement a été validé
        # Créer une commande après le paiement réussi
        total_price = sum(item.videoGame.price * item.quantity for item in cart_items)

        order = Order.objects.create(
            customuser=request.user,
            total_price=total_price,
            status='completed',  # Statut de commande
            stripe_session_id=session_id  # ID de session Stripe
        )

        # Insertion manuelle des articles de commande dans OrderItem
        with connection.cursor() as cursor:
            for item in cart_items:
                # Insérer manuellement dans la table djangoProject_orderitem
                cursor.execute(
                    '''
                    INSERT INTO public."djangoProject_orderitem"(
    quantity, order_id, "videoGame_id")
                    VALUES (%s, %s, %s)
                    ''', [order.id, item.videoGame.id, item.quantity]
                )
            # Réduire le stockù
        game = get_object_or_404(VideoGame, id=item.videoGame.id)
        game.stock -= int(item.quantity)
        game.save()

        # Vider le panier après la création de la commande
        cart.delete()

        # Rediriger vers une page de confirmation de commande
        return render(request, 'djangoProject/success.html', {'order': order})

    # Si le paiement a échoué
    return redirect('cancel')


@login_required
def payment_cancel(request):
    return render(request, 'djangoProject/cancel.html')


@login_required
@login_required
def order_history(request):
    # Récupérer toutes les commandes de l'utilisateur connecté
    orders = Order.objects.filter(customuser=request.user).order_by('-created_at')

    return render(request, 'djangoProject/order_history.html', {'orders': orders})


from django.shortcuts import render, get_object_or_404
from .models import Order, OrderItem  # Assurez-vous d'importer les modèles nécessaires

@login_required
def order_details(request, order_id):
    # Récupérer la commande par son ID
    order = get_object_or_404(Order, id=order_id, customuser=request.user)

    # Récupérer les items de la commande
    order_items = list(OrderItem.objects.filter(order=order))  # Récupérer les items sous forme de liste

    return render(request, 'djangoProject/order_details.html', {
        'order': order,
        'order_items': order_items
    })

@login_required
def order_item_details(request, order_id, video_game_id):
    # Récupérer l'élément de commande en fonction de l'ID de la commande et de l'ID du jeu vidéo
    order_item = get_object_or_404(OrderItem, order_id=order_id, videoGame_id=video_game_id)

    return render(request, 'djangoProject/order_item_details.html', {'order_item': order_item})