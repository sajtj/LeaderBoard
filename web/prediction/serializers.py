from rest_framework import serializers
from .models import Game, GamesLeaderBoard, Prediction

class GameDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = "__all__"
        # fields = [
        #     'id',
        #     'home_team',
        #     'away_team',
        #     'home_team_goals',
        #     'away_team_goals',
        #     'game_date',
        #     'status',
        # ]
        

class InputPredictionSerializer(serializers.ModelSerializer) :
    class Meta:
        model = Prediction
        fields = [
            'id',
            'exact_prediction',
            'home_team_goals_prediction',
            'away_team_goals_prediction',
            'general_prediction'
        ]
        
    def validate(self, attrs):
        general_prediction = attrs.get("general_prediction")
        exact_prediction = attrs.get("exact_prediction")
        home_team_goals_prediction = attrs.get("home_team_goals_prediction")
        away_team_goals_prediction = attrs.get("away_team_goals_prediction")
        
        if exact_prediction is None and general_prediction is None :
            raise serializers.ValidationError("select exact_prediction or general_prediction pls.")
        
        if exact_prediction is True and ((home_team_goals_prediction or away_team_goals_prediction) is None) :
            raise serializers.ValidationError("select home_team_goals_prediction and away_team_goals_prediction pls.")
        
        if general_prediction is not None and (((home_team_goals_prediction or away_team_goals_prediction) is not None) or (exact_prediction is True)):
            raise serializers.ValidationError("select one of exact_prediction or general_prediction pls.")
        
        return attrs
            
