from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    release_date = models.DateField()
    image_path = models.CharField(max_length=255)
    # Champ pour le chemin d'image
class CustomUser(models.Model):
    first_name = models.CharField(max_length=30)  # Champ pour le prénom
    last_name = models.CharField(max_length=30)   # Champ pour le nom
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('developer', 'Developer'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    numero_utilisateur = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.title