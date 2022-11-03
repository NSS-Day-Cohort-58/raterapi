from datetime import date
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from raterapi.models import GameCategory, Category, Game, GameReview

class ReviewView(ViewSet):
    """Review view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game review
        Returns:
            Response -- JSON serialized game type
        """
        review = GameReview.objects.get(pk=pk)
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
        review = GameReview()
        review.user = request.auth.user
        review.game = Game.objects.get(pk=request.data['gameId'])
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