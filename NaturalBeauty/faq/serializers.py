from rest_framework import serializers

from faq.models import Category, Faq


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'description', 'image')


class FaqSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Faq
        fields = ('question', 'response', 'locked')

# EOF
