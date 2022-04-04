from rest_framework import serializers

from webapp.models import Quote


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ('id', 'name', 'text', 'email', 'rate', 'is_status', 'created_at')
        read_only_fields = ('id', 'is_status', 'rate', 'created_at')

# {"name" : "API Create", "text": "GoodTextApi", "email" : "api@api.ru"}
# class ArticleCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Article
#         fields = ('id', 'title', 'content', 'author_id', 'created_at', 'updated_at')
#         read_only_fields = ('id', 'created_at', 'updated_at')