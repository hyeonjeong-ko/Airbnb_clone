from rest_framework.serializers import ModelSerializer
from categories.serializers import CategorySerializer
from users.serializers import TinyUserSerializer
from .models import Perk, Experiences


class PerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"


class ExperienceSerializer(ModelSerializer):
    host = TinyUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    perks = PerkSerializer(read_only=True)

    class Meta:
        model = Experiences
        fields = "__all__"
