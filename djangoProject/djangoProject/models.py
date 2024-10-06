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
    image = models.ImageField(upload_to='game_images/')
    stock = models.IntegerField()
    release_date = models.DateField()
    platform = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.title

# Modèle Order
from django.db import models

from django.db import models

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
    stripe_session_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} by {self.customuser.username}"

    def get_order_items(self):
        return OrderItem.objects.filter(order=self)  # Retourne tous les items associés à cette commande


class OrderItem(models.Model):
    videoGame = models.ForeignKey(VideoGame, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['order', 'videoGame'], name='unique_order_item')  # Clé unique pour order et videoGame
        ]

# Modèle Cart
class Cart(models.Model):
    customuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.customuser.username}"


# Modèle CartItem avec clé primaire composée
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')  # 'items' pour accéder aux articles du panier
    videoGame = models.ForeignKey(VideoGame, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cart', 'videoGame'], name='unique_cart_item')  # Clé composée (cart et videoGame)
        ]

# Modèle ADD (représentant un lien entre customuser et videoGame)
class Add(models.Model):
    customuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    videoGame = models.ForeignKey(VideoGame, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('customuser', 'videoGame')
