from datetime import date
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from raterapi.models import GameCategory, Category, Game

class CategoryView(ViewSet):
    """Category view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game category
        Returns:
            Response -- JSON serialized game type
        """
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"message": "The category you requested does not exist"}, status = status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category)
        return Response(serializer.data, status = status.HTTP_200_OK)



    def list(self, request):
        """Handle GET requests to get all categorys

        Returns:
            Response -- JSON serialized list of categorys
        """
        categorys = Category.objects.all()
        serializer = CategorySerializer(categorys, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Category
        fields = ('id', 'description', )