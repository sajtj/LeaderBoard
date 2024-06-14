from rest_framework import views, response, status, permissions
from drf_spectacular.utils import extend_schema
from .models import GamesLeaderBoard, Game
from .serializers import GameDetailSerializer, InputPredictionSerializer
from .permissions import GamePermissions


class GamesLeaderBoardAPIView(views.APIView) :
    permission_classes = (permissions.IsAuthenticated, )
    
    @extend_schema(
        responses={200: GameDetailSerializer(many=True)}
    )
    def get(self, request, pk_l) :
        games_leaderboard = GamesLeaderBoard.objects.get(id=pk_l)
        games = games_leaderboard.games.all()
        serializer = GameDetailSerializer(instance=games, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

class GameDetailAPIView(views.APIView) :
    permission_classes = (permissions.IsAuthenticated, GamePermissions, )
    
    @extend_schema(
        responses={200: GameDetailSerializer}
    )
    def get(self, request, pk_l, pk_g) :
        games_leaderboard = GamesLeaderBoard.objects.get(id=pk_l)
        game = games_leaderboard.games.get(id=pk_g)
        serializer = GameDetailSerializer(instance=game)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
    
    
    @extend_schema(
    request=InputPredictionSerializer,
    responses={201: InputPredictionSerializer},
    )
    def post(self, request, pk_l, pk_g) : # prediction
        user = request.user
        game = Game.objects.get(id=pk_g)
        self.check_object_permissions(request, game)
        leaderboard = GamesLeaderBoard.objects.get(id=pk_l)
        serializer = InputPredictionSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True) :
            serializer.save(user=user, game_prediction=game, games_leaderboard=leaderboard)
            return response.Response(status=status.HTTP_201_CREATED)
        
            
class UsersLeaderBoardAPIView(views.APIView) :
    permission_classes = (permissions.IsAuthenticated, )
    
    @extend_schema(
        responses={200: 'OK.'}
    )
    def get(self, request, pk_l) :
        games_leaderboard = GamesLeaderBoard.objects.get(id=pk_l)
        data = games_leaderboard.games_leaderboard_scoresheet
        return response.Response(data, status=status.HTTP_200_OK)
