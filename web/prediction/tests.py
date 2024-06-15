# poetry run python -m web.manage dumpdata accounts > web/prediction/fixtures/users.json
# poetry run python -m web.manage dumpdata  prediction.Team > web/prediction/fixtures/teams.json
# poetry run python -m web.manage dumpdata prediction.Game > web/prediction/fixtures/games.json
# poetry run python -m web.manage dumpdata prediction.GamesLeaderBoard > web/prediction/fixtures/gamesleaderboard.json
# poetry run python -m web.manage test web.prediction
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from .models import Team, Game, GamesLeaderBoard, Prediction, ResultStatus, GameStatus
from django.contrib.auth import get_user_model

User = get_user_model()

class IntegrationTests(APITestCase):
    fixtures = ['users.json', 'teams.json', 'games.json', 'gamesleaderboard.json']

    def setUp(self):
        self.client = APIClient()
        
        self.sajad = User.objects.get(username='sajad')
        self.aref = User.objects.get(username='aref')
        self.matin = User.objects.get(username='matin')
        self.mmreza = User.objects.get(username='mmreza')


        self.team1 = Team.objects.get(pk=1)
        self.team2 = Team.objects.get(pk=2)
        self.team3 = Team.objects.get(pk=3)
        self.team4 = Team.objects.get(pk=4)
        
        self.game1 = Game.objects.get(pk=5) # NS
        self.game2 = Game.objects.get(pk=6) # OP
        
        self.leaderboard = GamesLeaderBoard.objects.get(pk=7)

    def test_get_games_leaderboard(self):
        self.client.force_authenticate(user=self.sajad)
        
        url = reverse('Game-LeaderBoard', kwargs={'pk_l': self.leaderboard.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['home_team'], self.team1.id)

    def test_get_game_detail(self):
        self.client.force_authenticate(user=self.sajad)
        
        url = reverse('Game-Detail', kwargs={'pk_l': self.leaderboard.id, 'pk_g': self.game1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['home_team'], self.team1.id)


    def test_prediction_validation(self):
        self.client.force_authenticate(user=self.sajad)
        
        url = reverse('Game-Detail', kwargs={'pk_l': self.leaderboard.id, 'pk_g': self.game1.id})
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        data = {
            'exact_prediction': True,
            'away_team_goals_prediction': 1
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
        data = {
            'exact_prediction': True,
            'home_team_goals_prediction': 2,
            'away_team_goals_prediction': 1
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) #  checkk
    
        url = reverse('Game-Detail', kwargs={'pk_l': self.leaderboard.id, 'pk_g': self.game2.id})    
        data = {
            'exact_prediction': True,
            'home_team_goals_prediction': 2,
            'away_team_goals_prediction': 1
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_prediction(self):
        self.client.force_authenticate(user=self.aref) # 15
        url = reverse('Game-Detail', kwargs={'pk_l': self.leaderboard.id, 'pk_g': self.game1.id})
        data = {
            'exact_prediction': True,
            'home_team_goals_prediction': 3,
            'away_team_goals_prediction': 2
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Prediction.objects.filter(user=self.aref, game_prediction=self.game1).exists())
        
        self.client.force_authenticate(user=self.mmreza) # 5
        url = reverse('Game-Detail', kwargs={'pk_l': self.leaderboard.id, 'pk_g': self.game1.id})
        data = {
            'exact_prediction': True,
            'home_team_goals_prediction': 1,
            'away_team_goals_prediction': 2
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Prediction.objects.filter(user=self.mmreza, game_prediction=self.game1).exists())
        
        self.client.force_authenticate(user=self.matin) # 10
        url = reverse('Game-Detail', kwargs={'pk_l': self.leaderboard.id, 'pk_g': self.game1.id})
        data = {
            'general_prediction': ResultStatus.HomeTeamWin
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Prediction.objects.filter(user=self.matin, game_prediction=self.game1).exists())
        
        self.client.force_authenticate(user=self.sajad) # 20
        url = reverse('Game-Detail', kwargs={'pk_l': self.leaderboard.id, 'pk_g': self.game1.id})
        data = {
            'exact_prediction': True,
            'home_team_goals_prediction': 2,
            'away_team_goals_prediction': 1
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Prediction.objects.filter(user=self.sajad, game_prediction=self.game1).exists())

        

    def test_leaderboard_update_on_game_end(self):
        self.client.force_authenticate(user=self.sajad) # 5
        url = reverse('User-LeaderBoard', kwargs={'pk_l': self.leaderboard.id})

        self.test_create_prediction()

        self.game1.status = GameStatus.Endded
        self.game1.home_team_goals = 2
        self.game1.away_team_goals = 1
        self.game1.result = ResultStatus.HomeTeamWin
        self.game1.save()

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['scoresheet'][0]['user'], self.sajad.username)
        self.assertEqual(response.data['scoresheet'][1]['user'], self.aref.username)
        self.assertEqual(response.data['scoresheet'][2]['user'], self.matin.username)
        self.assertEqual(response.data['scoresheet'][3]['user'], self.mmreza.username)

