from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
User = get_user_model()


class GameStatus(models.TextChoices):
    NotStarted = 'NS', 'Not Started'
    OnPerforming = 'OP', 'On Performing'
    Endded = 'EN', 'Endded'

class ResultStatus(models.TextChoices):
    HomeTeamWin = 'HTW', 'Home Team Win'
    HomeTeamLose = 'HTL', 'Home Team Lose'
    AwayTeamWin = 'ATW', 'Away Team Win'
    AwayTeamLose = 'ATL', 'Away Team Lose'
    Draw = 'D', 'Draw'

class Team(models.Model) :
    name = models.CharField(max_length=256)
    
    def __str__(self):
        return self.name
 
    
class Game(models.Model) :
    home_team = models.ForeignKey(Team, related_name='home_games', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_games', on_delete=models.CASCADE)
    home_team_goals = models.IntegerField(null=True, blank=True)
    away_team_goals = models.IntegerField(null=True, blank=True)
    game_date = models.DateTimeField()
    status = models.CharField(
        max_length=2,
        choices=GameStatus.choices,
        default=GameStatus.NotStarted,
    )
    result = models.CharField(max_length=3, choices=ResultStatus.choices, null=True, blank=True)
    
    def clean(self) :
        if self.home_team == self.away_team:
            raise ValidationError({'away_team': 'Home team and away team must be different.'})
        
    def __str__(self) :
        return f"{self.home_team} Vs {self.away_team} - {self.status}"


class GamesLeaderBoard(models.Model) :
    games = models.ManyToManyField(Game, related_name='leaderboard')
    games_leaderboard_scoresheet = models.JSONField(default=dict, null=True, blank=True)

class Prediction(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_prediction = models.ForeignKey(Game, on_delete=models.CASCADE)
    games_leaderboard = models.ForeignKey(GamesLeaderBoard, on_delete=models.CASCADE)
    exact_prediction = models.BooleanField(default=False)
    home_team_goals_prediction = models.PositiveIntegerField(null=True, blank=True)
    away_team_goals_prediction = models.PositiveIntegerField(null=True, blank=True)
    general_prediction = models.CharField(max_length=3, choices=ResultStatus.choices, null=True, blank=True)
    score = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
