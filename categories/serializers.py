from rest_framework import serializers
#from rest_framework.serializers import ModelSerializer
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
