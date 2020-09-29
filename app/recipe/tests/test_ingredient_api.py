from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient, Recipe
from recipe.serializers import IngredientSerializer

INGREDIENT_URL = reverse('recipe:ingredient-list')


def sample_recipe(name, description):
    """
    Creates a sample recipe
    """
    recipe = Recipe.objects.create(
        name=name,
        description=description)
    return recipe


def sample_ingredient(name, recipe):
    """
    Creates a sample ingredient
    """
    ingredient = Ingredient.objects.create(
        name=name,
        recipe=recipe
    )
    return ingredient


def detail_url(recipe_id):
    return reverse('recipe:ingredient-detail', args=[recipe_id])


class IngredientApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_list_ingredients(self):
        """
        Tests that ingredients can be retrieved
        """
        recipe = sample_recipe("Spaghetti bolognesa",
                               "Pasta with meat and tomato sauce")
        sample_ingredient("Spaghetti", recipe)
        sample_ingredient("Meat", recipe)

        res = self.client.get(INGREDIENT_URL)

        ingredients = Ingredient.objects.all().order_by('name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_ingredient(self):
        """
        Tests that an ingredient can be created
        """
        recipe = sample_recipe("Spaghetti bolognesa",
                               "Pasta with meat and tomato sauce")
        payload = {
            "name": "Spaghetti",
            "recipe": recipe.id
        }

        res = self.client.post(INGREDIENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        exists = Ingredient.objects.filter(name=payload['name']).exists()
        self.assertTrue(exists)

    def test_update_ingredient(self):
        """
        Tests that an ingredient can be updated
        """

        recipe = sample_recipe("Spaghetti bolognesa",
                               "Pasta with meat and tomato sauce")
        ingredient = sample_ingredient("Spaghetti", recipe)

        payload = {
            'name': 'Pasta'
        }

        url = detail_url(ingredient.id)
        res = self.client.patch(url, payload)

        ingredient.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(ingredient.name, payload['name'])

    def test_delete_ingredient(self):
        """
        Tests that an ingredient can be deleted
        """

        recipe = sample_recipe("Spaghetti bolognesa",
                               "Pasta with meat and tomato sauce")
        ingredient = sample_ingredient("Spaghetti", recipe)

        url = detail_url(ingredient.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        ingredients = Ingredient.objects.all()
        self.assertEqual(len(ingredients), 0)
