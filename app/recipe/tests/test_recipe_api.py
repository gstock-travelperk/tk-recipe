from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Ingredient
from recipe.serializers import RecipeSerializer

RECIPE_URL = reverse('recipe:recipe-list')


def sample_recipe(name, description):
    """
    Creates a sample recipe
    """
    recipe = Recipe.objects.create(
        name=name,
        description=description)
    return recipe


class RecipeApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_list_recipes(self):
        """
        Tests that recipes are listes correctly
        """

        sample_recipe("Pizza", "Pizza with cheese")
        sample_recipe("Soup", "Onion soup")

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all().order_by('name')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe_successful(self):
        """
        Tests that a recipe can be created
        """

        payload = {
            'name': 'Vegan Pizza',
            'description': 'Pizza with artificial cheese'
        }

        res = self.client.post(RECIPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        exists = Recipe.objects.filter(name=payload['name']).exists()
        self.assertTrue(exists)

    def test_create_recipe_invalid(self):
        """
        Tests that a recipe cannot be created without a name
        """

        payload = {
            'name': '',
        }

        res = self.client.post(RECIPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
