from rest_framework import serializers
from .models import SearchInteraction, ImageInteraction


class ImageSearchRequestSerializer(serializers.Serializer):
    query = serializers.CharField(required=True, max_length=500)
    top_k = serializers.IntegerField(
        required=False, default=5, min_value=1, max_value=100)


class ImageSearchResultSerializer(serializers.Serializer):
    path = serializers.CharField()
    similarity = serializers.FloatField()


class ImageSearchResponseSerializer(serializers.Serializer):
    results = ImageSearchResultSerializer(many=True)


class DatasetInfoSerializer(serializers.Serializer):
    status = serializers.CharField()
    exists = serializers.BooleanField()
    image_count = serializers.IntegerField()
    data_path = serializers.CharField()


class SearchInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchInteraction
        fields = '__all__'


class ImageInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageInteraction
        fields = '__all__'
