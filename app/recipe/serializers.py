from rest_framework import serializers
from core.models import Ingredient, Recipe


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


class RecipeSerializer(serializers.ModelSerializer):

    ingredients = BasicIngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'ingredients')
        read_only_fields = ('id',)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        recipe = Recipe.objects.create(**validated_data)
        if ingredients:
            recipe_ingredientes = [Ingredient(
                recipe=recipe, **ingredient) for ingredient in ingredients]
            Ingredient.objects.bulk_create(recipe_ingredientes)
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.save()
        ingredients = validated_data.pop('ingredients', None)
        if ingredients:
            Ingredient.objects.filter(recipe=instance).delete()
            recipe_ingredientes = [Ingredient(
                recipe=instance, **ingredient) for ingredient in ingredients]
            Ingredient.objects.bulk_create(recipe_ingredientes)
        return instance


class RecipeDetailSerializer(RecipeSerializer):
    ingredients = BasicIngredientSerializer(many=True, read_only=True)
