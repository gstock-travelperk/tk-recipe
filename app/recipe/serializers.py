from rest_framework import serializers
from core.models import Ingredient, Recipe


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description')
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):

    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'recipe')
        read_only_fields = ('id',)
