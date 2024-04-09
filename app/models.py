# Models for Nomic game entities

from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class GameState(models.Model):
    state = models.JSONField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'State {self.id} - Active: {self.active}'

# Future models and game entities can be added here.