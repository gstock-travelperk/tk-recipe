from rest_framework import serializers
from core.models import Ingredient, Recipe


class RecipeSerializer(serializers.ModelSerializer):

    ingredients = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'ingredients')
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):

    recipe = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all())

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'recipe')
        read_only_fields = ('id',)


class BasicIngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeDetailSerializer(RecipeSerializer):
    ingredients = BasicIngredientSerializer(many=True, read_only=True)
