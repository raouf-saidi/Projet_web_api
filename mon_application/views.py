from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Game
from .serializers import GameSerializer
# Create your views here.
from django.http import HttpResponse

def index(request):
    return render(request, 'template/index.html')

def home(request):
    return render(request, 'template/index.html')

def shop(request):
    return render(request, 'template/shop.html')

def product_details(request):
    return render(request, 'template/product_details.html')

def contact(request):
    return render(request, 'template/contact.html')

def sign_in(request):
    return render(request, 'template/contact.html')

# views.py

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]  # Nécessite une authentification

    def perform_create(self, serializer):
        # Assurez-vous que l'utilisateur est un admin avant de créer un jeu
        if self.request.user.role == 'admin':
            serializer.save(user=self.request.user)  # Associe le jeu à l'utilisateur actuel
        else:
            raise permissions.PermissionDenied("Vous n'avez pas la permission d'ajouter un jeu.")

    def perform_update(self, serializer):
        # Assurez-vous que l'utilisateur est un admin avant de modifier un jeu
        if self.request.user.role == 'admin':
            serializer.save()
        else:
            raise permissions.PermissionDenied("Vous n'avez pas la permission de modifier ce jeu.")

    def perform_destroy(self, instance):
        # Assurez-vous que l'utilisateur est un admin avant de supprimer un jeu
        if self.request.user.role == 'admin':
            instance.delete()
        else:
            raise permissions.PermissionDenied("Vous n'avez pas la permission de supprimer ce jeu.")
