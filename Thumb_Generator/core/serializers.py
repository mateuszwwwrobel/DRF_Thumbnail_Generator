from rest_framework import serializers
from core.models import Image


class ImageCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['original_size_image']


class BasicPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['image_200px']


class PremiumPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['original_size_image', 'image_200px', 'image_400px']


class EnterprisePlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['original_size_image', 'image_200px', 'image_400px']


class CustomPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['original_size_image', 'image_200px', 'image_400px', 'image_custom_size']
