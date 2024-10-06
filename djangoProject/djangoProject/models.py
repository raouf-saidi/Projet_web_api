from django.db import models
from django.contrib.auth.models import AbstractUser

# Utilisateur personnalisé (customuser) qui hérite du modèle utilisateur de Django
class CustomUser(AbstractUser):
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

# Modèle Role
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Modèle VideoGame
class VideoGame(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=255)
    stock = models.IntegerField()
    release_date = models.DateField()
    platform = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.title

# Modèle Order
class Order(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('pending', 'Pending'),
    ]
    customuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    def __str__(self):
        return f"Order {self.id} by {self.customuser.username}"

# Modèle OrderItem
class OrderItem(models.Model):
    videoGame = models.ForeignKey(VideoGame, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()

# Modèle Cart
class Cart(models.Model):
    customuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

# Modèle CartItem
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    videoGame = models.ForeignKey(VideoGame, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    class Meta:
        unique_together = (('cart', 'videoGame'),)  # Définir la clé primaire composite

    def __str__(self):
        return f"{self.videoGame.title} in cart {self.cart.id}"

# Modèle ADD (représentant un lien entre customuser et videoGame)
class Add(models.Model):
    customuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    videoGame = models.ForeignKey(VideoGame, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('customuser', 'videoGame')

