from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


def user_directory_path(instance, filename):
    return f"user_{instance.user.id}/{filename}"


# =========================
# PROFILE
# =========================

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    profile_picture = models.ImageField(
        upload_to=user_directory_path,
        default="default_profile.png"
    )

    def __str__(self):
        return f"{self.user.username} Profile"



# =========================
# PRODUCT
# =========================

class Product(models.Model):
    PLATFORM_CHOICES = [
        ("Facebook", "Facebook"),
        ("Instagram", "Instagram"),
        ("Twitter", "Twitter"),
        ("TikTok", "TikTok"),
        ("Snapchat", "Snapchat"),
    ]

    TYPE_CHOICES = [
        ("Personal", "Personal"),
        ("Business", "Business"),
    ]

    name = models.CharField(max_length=100)

    platform = models.CharField(
        max_length=20,
        choices=PLATFORM_CHOICES,
        default="Instagram",
        db_index=True
    )

    account_year = models.PositiveIntegerField(default=2020)

    account_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default="Personal"
    )

    followers = models.PositiveIntegerField(
        blank=True,
        null=True,
        default=0
    )

    stock = models.PositiveIntegerField(default=1)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.platform} | {self.name}"


# =========================
# ORDER
# =========================

class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


# =========================
# TRANSACTION
# =========================

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("fund", "Added Funds"),
        ("purchase", "Purchase"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="transactions"
    )
    type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=100, unique=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.user.username} | {self.type} | {self.amount}"

