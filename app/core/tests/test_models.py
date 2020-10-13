from django.test import TestCase
from core import models


def sample_recipe(name, description):
    """
    Creates a sample recipe
    """
    recipe = models.Recipe.objects.create(
        name=name,
        description=description)
    return recipe


class ModelTests(TestCase):
    """
    Contains all the model tests
    """

    def test_recipe(self):
        """
        Tests the recipe model
        """
        recipe = sample_recipe(
            name='Chicken salami',
            description='Chicken breast with salami')
        self.assertEqual(str(recipe), recipe.name)

    def test_ingredient(self):
        """
        Tests the ingredient model
        """
        recipe = sample_recipe('Chicken salad', 'A chicken inside a salad')
        ingredient = models.Ingredient.objects.create(
            name='Chicken',
            recipe=recipe
        )

        self.assertEqual(str(ingredient), ingredient.name)
