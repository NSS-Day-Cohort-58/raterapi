from datetime import date

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from raterapi.models import Category, Game, GameRating


class RatingView(ViewSet):
    """Review view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game review
        Returns:
            Response -- JSON serialized game type
        """
        try:
            review = GameRating.objects.get(pk=pk)
        except GameRating.DoesNotExist:
            return Response({"message": "The game rating you requested does not exist"}, status = status.HTTP_404_NOT_FOUND)

        serializer = RatingSerializer(review)
        return Response(serializer.data, status = status.HTTP_200_OK)



    def list(self, request):
        """Handle GET requests to get all reviews

        Returns:
            Response -- JSON serialized list of reviews
        """
        reviews = GameRating.objects.all()
        serializer = RatingSerializer(reviews, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        required_fields = ['gameId', 'rating']
        missing_fields = 'Hey dummy, you are missing'
        is_field_missing = False

        for field in required_fields:
            value = request.data.get(field, None)

            if value is None:
                missing_fields = f'{missing_fields} and {field}'
                is_field_missing = True

        if is_field_missing:
            return Response({"message": missing_fields}, status = status.HTTP_400_BAD_REQUEST)

        # Validate rating between 1 and 10
        rating_from_client_request = request.data.get("rating")

        try:
            if rating_from_client_request > 10 or rating_from_client_request < 1:
                return Response({"message": 'Rating must be between 1 and 10'}, status = status.HTTP_400_BAD_REQUEST)
        except TypeError:
            return Response({"message": 'Rating must be an integer'}, status = status.HTTP_400_BAD_REQUEST)

        try:
            assigned_game = Game.objects.get(pk=request.data['gameId'])
        except Game.DoesNotExist:
            return Response({"message": "The game you specified does not exist"}, status = status.HTTP_404_NOT_FOUND)

        review = GameRating()
        review.user = request.auth.user
        review.game = assigned_game
        review.rating = request.data['rating']
        review.created_on = date.today()
        review.save()


        serializer = RatingSerializer(review)
        return Response(serializer.data, status = status.HTTP_201_CREATED)


class RatingSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = GameRating
        fields = ('id', 'user', 'game', 'rating', 'created_on',)
