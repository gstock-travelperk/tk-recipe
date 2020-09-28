from rest_framework import viewsets

from core.models import Recipe, Ingredient
from recipe.serializers import RecipeSerializer, IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_queryset(self):
        return self.queryset.order_by('name')


class IngredientViewSet(viewsets.ModelViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get_queryset(self):
        return self.queryset.order_by('name')
