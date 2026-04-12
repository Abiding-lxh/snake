from django.contrib import admin
from game.models.player import Player
from game.models.bot import Bot
# Register your models here.

admin.site.register(Player)
admin.site.register(Bot)