from rest_framework import permissions, exceptions
from django.utils import timezone

class GamePermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, game):
        
        if timezone.now() > game.game_date :
            raise exceptions.PermissionDenied({"msg" : "Match already started."})
        else:
            return True   