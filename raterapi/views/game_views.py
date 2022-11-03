from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from raterapi.models import GameCategory, Category, Game

class GameView(ViewSet):
    """game rater game view"""



    # get singular game
    def retrieve(self, request, pk):
        """Handle GET requests for single game type
        Returns:
            Response -- JSON serialized game type
        """
        game = Game.objects.get(pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data, status = status.HTTP_200_OK)

        
        

    # get all games
    def list(self, request):
        """Handle GET requests to get all games

        Returns:
            Response -- JSON serialized list of games
        """
        # select *
        # from levelupapi_gametype
        game = Game.objects.all()
        serializer = GameSerializer(game, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    # create a game 
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        
        game = Game.objects.create(
            user=request.auth.user,
            title=request.data["title"],
            release_year=request.data["releaseYear"],
            image_file=request.data["imageFile"],
            number_of_players=request.data["numberOfPlayers"],
            description=request.data["description"],
            designer=request.data["designer"],
            time_to_play=request.data["timeToPlay"],
            recommended_age=request.data["recommendedAge"]
        )
        

        # We have a pk for the new game, create GameCategory instances
        categories = request.data["categories"]
        for category in categories:
            category_to_assign = Category.objects.get(pk=category)
            
            game_category = GameCategory()
            game_category.game = game
            game_category.category = category_to_assign
            game_category.save()

        
        serializer = GameSerializer(game)
        return Response(serializer.data, status = status.HTTP_201_CREATED)

    

class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Game
        fields = ('id', 'user', 'title', 'release_year', 'image_file', 'number_of_players', 'description', 
                    'designer', 'time_to_play', 'recommended_age', 'categories')