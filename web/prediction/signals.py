from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Game, Prediction
from .utils import redis_connection

redis_client = redis_connection()

def calculate_score(prediction, game):
    if prediction.exact_prediction:
        if (prediction.home_team_goals_prediction == game.home_team_goals and prediction.away_team_goals_prediction == game.away_team_goals):
            return 20
        elif (prediction.home_team_goals_prediction - prediction.away_team_goals_prediction) == (game.home_team_goals - game.away_team_goals) :
            return 15
    
    if prediction.general_prediction == game.result:
        return 10 
    
    return 5

def update_user_score_in_redis(user, score, cache_key):
    redis_client.zincrby(cache_key, score, user.username)
    
def sorted_users(cache_key) :
    users_sorted = redis_client.zrevrange(cache_key, 0, -1, withscores=True)
    return users_sorted

@receiver(post_save, sender=Game)
def update_game_status(sender, instance, created, **kwargs):
    if not created and instance.status == 'EN':
        predictions = Prediction.objects.filter(game_prediction=instance)
        games_leaderboard = predictions.first().games_leaderboard
        cache_key = "leaderboard_" + str(games_leaderboard.id)
        
        for prediction in predictions:
            user = prediction.user
            score = calculate_score(prediction, instance)
            update_user_score_in_redis(user, score, cache_key)
        
        users_sorted = sorted_users(cache_key)
        result = [{'user': user, 'score': score} for user, score in users_sorted]
        games_leaderboard.games_leaderboard_scoresheet = {"scoresheet": result}
        games_leaderboard.save()
        
            

