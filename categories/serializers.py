from rest_framework import serializers
from .models import Category

# sirializer에게 보여줄 feature 명시
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        # exclude = ("created_at",)
