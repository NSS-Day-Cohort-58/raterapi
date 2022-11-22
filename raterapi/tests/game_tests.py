import json
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from raterapi.models import Game

class GameTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens',  'games', 'categories']

    def setUp(self):
        # Grab the first Gamer object from the database and add their token to the headers
        self.gamer = User.objects.first()
        token = Token.objects.get(user=self.gamer)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_game(self):
        """Create game test"""
        url = "/games"

        # Define the Game properties
        # The keys should match what the create method is expecting
        # Make sure this matches the code you have
        game = {
            "title": "Clue",
            "releaseYear": 2022,
            "imageFile": "",
            "description": "Whodunit",
            "designer": "Tiana",
            "numberOfPlayers": 7,
            "timeToPlay": 1900,
            "recommendedAge": 54,
            "categories": [1,2]
        }

        response = self.client.post(url, game, format='json')
        response_json = json.loads(response.content)


        self.assertIn('id', response_json)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(response_json["title"], "Clue")
        self.assertEqual(response_json["average_rating"], 0)
        self.assertEqual(response_json["release_year"], 2022)
        self.assertEqual(response_json["image_file"], "")
        self.assertEqual(response_json["number_of_players"], 7)
        self.assertEqual(response_json["description"], "Whodunit")
        self.assertEqual(response_json["designer"], "Tiana")
        self.assertEqual(response_json["time_to_play"], 1900)
        self.assertEqual(response_json["recommended_age"], 54)
        self.assertEqual(response_json["user"], 1)
        self.assertEqual(response_json["reviews"], [])
        self.assertEqual(response_json["categories"], [{'description': 'Strategy'}, {'description': 'Dice'}])
