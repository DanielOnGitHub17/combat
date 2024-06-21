import datetime

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

num_valid = lambda x, y: [MinValueValidator(x), MaxValueValidator(y)]

# Create your models here.
class Game(models.Model):
    size = models.IntegerField(default=15)
    initial_data = models.TextField(default="0")
    data = models.TextField(default="0") # will change by json.loadsing and dumpsing
    count = models.IntegerField(default=2, validators=num_valid(2, 7))
    max_hits = models.IntegerField(default=3, validators=num_valid(2, 7))
    started_time = models.DateTimeField(default=datetime.time())
    ended_time = models.DateTimeField(default=datetime.time())
    started = models.BooleanField(default=False)
    ended = models.BooleanField(default=False)
    # primary key should be the link slash. (it will always change)
    # do passcode later for private games - join with passcode...
    # It will be so cool, the passcode becomes invalid when game starts

    @property
    def available(self):
        return not (self.started or self.ended)

    @property
    def ongoing(self):
        return self.started and not self.ended

    @property
    def players(self):
        return Player.objects.filter(game=self)
    
    @property
    def n(self):
        return len(self.players)

    def __str__(self):
        return f"Game {self.pk}"
    
    def get_absolute_url(self):
        return f"/game/{self.id}/"

    # The Game class will be frequently accessed by users, changed till there are no
    # '1s' in it's data.
    # if needed, the Game class will be turned to JSON later

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.PROTECT, null=True, blank=True)
    logged_in = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    r = models.IntegerField(default=0)
    c = models.IntegerField(default=0)
    winner = models.BooleanField(default=False)
    won = models.IntegerField(default=0)
    creator = models.BooleanField(default=False)
    # will be given by difference between game.started and ended
    # (or game.started and logged out) Logout will have some work to do
    # it will have to check if the player was playing before he/she left
    # and other loopholes I will have to fill.

    @property
    def rank(self):
        return 2*self.won
    
    @property
    def full_name(self):
        return self.user.get_full_name()

    def __str__(self):
        return self.full_name
    
    def get_absolute_url(self):
        return f"/player/{self.id}/"
