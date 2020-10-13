from rest_framework import viewsets

from core.models import Recipe, Ingredient
from recipe.serializers import RecipeSerializer, IngredientSerializer, RecipeDetailSerializer


class RecipeViewSet(viewsets.ModelViewSet):

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_queryset(self):
        return self.queryset.order_by('name')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RecipeDetailSerializer
        return self.serializer_class


class IngredientViewSet(viewsets.ModelViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get_queryset(self):
        return self.queryset.order_by('name')
