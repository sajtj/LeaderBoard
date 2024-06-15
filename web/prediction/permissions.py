from rest_framework import permissions, exceptions
from django.utils import timezone
from .models import GameStatus

class GamePermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, game):
        
        if timezone.now() > game.game_date and game.status == GameStatus.OnPerforming:
            raise exceptions.PermissionDenied({"msg" : "Match already started."})
        elif timezone.now() > game.game_date and game.status == GameStatus.Endded:
            raise exceptions.PermissionDenied({"msg" : "Match already finished."})
        else:
            return True   