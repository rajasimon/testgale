from rest_framework import serializers

from testgale.core.models import Crawler, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class CrawlerSerializer(serializers.ModelSerializer):
    # To fetch multiple images
    image_set = ImageSerializer(many=True)

    class Meta:
        model = Crawler
        fields = ['id', 'url', 'image_set']
