from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.core.validators import MaxValueValidator
# Create your models here.


class User(AbstractUser):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    username = models.CharField(max_length=50, null=True, default="John")
    email = models.EmailField(unique=True, null=False)
    phone = models.CharField(max_length=14)
    avatar = models.ImageField(default='avatar.jpeg', null=True)
    created = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']


class Staff(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    field = models.CharField(max_length=50, null=False)
    date_of_birth = models.DateField()
    avatar = models.ImageField(default="avatar.jpeg", null=False)

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Rating(models.Model):
    value = models.IntegerField(default=0, validators=[MaxValueValidator(10)])

class NewsPage(models.Model):
    headline = models.CharField(max_length=150, null=False)
    author = models.CharField(max_length=60, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)
    main_image = models.ImageField(null=True, default="avatar.jpeg")
    main_image_title = models.CharField(max_length=120, null=False)
    sub_image = models.ImageField(null=True, default="avatar.jpeg")
    sub_image_title = models.CharField(max_length=120, null=False)
    news_content = models.TextField(null=False)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

class Comment(models.Model):
    text =  models.TextField(blank=False)
    news_page = models.ForeignKey(NewsPage, on_delete=models.CASCADE, null=False)