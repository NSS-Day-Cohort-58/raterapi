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

    def test_delete_game(self):
        """
        Ensure we can delete an existing game.
        """
        game = Game()
        game.release_year = 1994
        game.title = "Trivial Pursuit"
        game.image_file = ""
        game.designer = "Hasbro"
        game.time_to_play = 40
        game.recommended_age = 13
        game.number_of_players = 4
        game.user_id = 1
        game.save()

        response = self.client.delete(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY 404 response
        response = self.client.get(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


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
