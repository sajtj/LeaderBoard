from django.contrib import admin
from .models import *

admin.site.register(Team)
admin.site.register(Game)
admin.site.register(GamesLeaderBoard)
admin.site.register(Prediction)