from datetime import date

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from raterapi.models import Category, Game, GameCategory, GameReview


class ReviewView(ViewSet):
    """Review view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game review
        Returns:
            Response -- JSON serialized game type
        """
        try:
            review = GameReview.objects.get(pk=pk)
        except GameReview.DoesNotExist:
            return Response({"message": "The game view you requested does not exist"}, status = status.HTTP_404_NOT_FOUND)

        serializer = ReviewSerializer(review)
        return Response(serializer.data, status = status.HTTP_200_OK)



    def list(self, request):
        """Handle GET requests to get all reviews

        Returns:
            Response -- JSON serialized list of reviews
        """
        reviews = GameReview.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        required_fields = ['gameId', 'review']
        missing_fields = 'Hey dummy, you are missing'
        is_field_missing = False

        for field in required_fields:
            value = request.data.get(field, None)
            if value is None:
                missing_fields = f'{missing_fields} and {field}'
                is_field_missing = True

        if is_field_missing:
            return Response({"message": missing_fields}, status = status.HTTP_400_BAD_REQUEST)

        try:
            assigned_game = Game.objects.get(pk=request.data['gameId'])
        except Game.DoesNotExist:
            return Response({"message": "The game you specified does not exist"}, status = status.HTTP_404_NOT_FOUND)

        review = GameReview()
        review.user = request.auth.user
        review.game = assigned_game
        review.review = request.data['review']
        review.created_on = date.today()
        review.save()


        serializer = ReviewSerializer(review)
        return Response(serializer.data, status = status.HTTP_201_CREATED)


class ReviewSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = GameReview
        fields = ('id', 'user', 'game', 'review', 'created_on',)
