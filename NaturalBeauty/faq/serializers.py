from rest_framework import serializers

from .models import Category, Response, Question


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'description', 'image')


class ResponseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Response
        fields = ('question', 'response', 'locked')


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Response
        fields = ('question', 'response', 'locked')

# EOF
