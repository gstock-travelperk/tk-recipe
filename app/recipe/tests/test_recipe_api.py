from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
import json

from core.models import Recipe
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


def detail_url(recipe_id):
    return reverse('recipe:recipe-detail', args=[recipe_id])


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
            'description': 'Pizza with artificial cheese',
            'ingredients': [{'name': 'cheese'}, {'name': 'dough'}]
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

    def test_update_recipe(self):
        """
        Tests that a recipe can be updated
        """

        recipe = sample_recipe("Beef mariachi", "Beef with a lot of chili")
        url = detail_url(recipe.id)

        payload = {
            "description": "Beef with a lot of chili sauce"
        }
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe.refresh_from_db()
        self.assertEqual(recipe.description, payload['description'])

    def test_update_recipe_ingredients(self):
        """
        Tests that a recipe can be updated
        """

        recipe = sample_recipe("Beef mariachi", "Beef with a lot of chili")
        url = detail_url(recipe.id)

        payload = {
            'description': 'Beef with a lot of chili sauce',
            'ingredients': [{'name': 'cheese'}, {'name': 'dough'}]
        }

        # res = self.client.patch(url, payload)
        res = self.client.patch(url, json.dumps(
            payload), content_type='application/json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe.refresh_from_db()
        ingredients = recipe.ingredients.all()
        self.assertEqual(len(ingredients), 2)

    def test_delete_recipe(self):
        """
        Tests that a recipe can be deleted
        """

        recipe = sample_recipe("Beef mariachi", "Beef with a lot of chili")
        url = detail_url(recipe.id)

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        recipes = Recipe.objects.all()
        self.assertEqual(len(recipes), 0)
