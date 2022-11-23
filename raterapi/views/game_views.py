from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
from raterapi.models import GameCategory, Category, Game, GameReview

class GameView(ViewSet):
    """game rater game view"""
    # e0f7eb3161752da6e6ccaa9170a8def97f7c4221

    def retrieve(self, request, pk):
        """Handle GET requests for single game type
        Returns:
            Response -- JSON serialized game type
        """
        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            return Response({"message": "The game you requested does not exist"}, status = status.HTTP_404_NOT_FOUND)

        serializer = GameSerializer(game)
        return Response(serializer.data, status = status.HTTP_200_OK)

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

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        required_fields = ['title', 'designer', 'categories',
                        'releaseYear', 'imageFile', 'numberOfPlayers',
                        'description', 'timeToPlay', 'recommendedAge']
        missing_fields = 'Hey dummy, you are missing'
        is_field_missing = False


        for field in required_fields:
            value = request.data.get(field, None)
            if value is None:
                missing_fields = f'{missing_fields} and {field}'
                is_field_missing = True

        if is_field_missing:
            return Response({"message": missing_fields}, status = status.HTTP_400_BAD_REQUEST)


        # We have a pk for the new game, create GameCategory instances
        categories = request.data["categories"]
        for category in categories:
            try:
                category_to_assign = Category.objects.get(pk=category)
            except Category.DoesNotExist:
                return Response({"message": "The category you specified does not exist"}, status = status.HTTP_404_NOT_FOUND)


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
        for category in categories:
            category_to_assign = Category.objects.get(pk=category)
            game_category = GameCategory()
            game_category.game = game
            game_category.category = category_to_assign
            game_category.save()


        serializer = GameSerializer(game)
        return Response(serializer.data, status = status.HTTP_201_CREATED)

    def delete(self, request, pk):
        try:
            game_to_delete = Game.objects.get(pk=pk)
            game_to_delete.delete()
            return Response(None, status = status.HTTP_204_NO_CONTENT)
        except Game.DoesNotExist:
            return Response(None, status = status.HTTP_404_NOT_FOUND)


class GameReviewUserSerializer(serializers.ModelSerializer):
    """JSON serializer for game review users """

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', )


class GameReviewsSerializer(serializers.ModelSerializer):
    """JSON serializer for game reviews """
    user = GameReviewUserSerializer(many=False)

    class Meta:
        model = GameReview
        fields = ('review', 'created_on', 'user', )


class GameCategoriesSerializer(serializers.ModelSerializer):
    """JSON serializer for game categories """

    class Meta:
        model = Category
        fields = ('description', )


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games """
    reviews = GameReviewsSerializer(many=True)
    categories = GameCategoriesSerializer(many=True)

    class Meta:
        model = Game
        fields = ('id', 'user', 'reviews', 'title', 'average_rating',
                  'release_year', 'image_file', 'number_of_players',
                  'description', 'designer', 'time_to_play',
                  'recommended_age', 'categories')
