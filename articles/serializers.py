from rest_framework import serializers
from .models import Article, Score
from django.core.cache import cache
from datetime import timedelta
from django.utils.timezone import now


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'num_scores', 'average_score']

    num_scores = serializers.SerializerMethodField()
    average_score = serializers.SerializerMethodField()

    def get_num_scores(self, obj):
        cache_key = f"article_{obj.id}_num_scores"
        num_scores = cache.get(cache_key)
        if num_scores is None:
            num_scores = obj.scores.count()
            cache.set(cache_key, num_scores, timeout=3600)  # Cache for 1 hour
        return num_scores

    def get_average_score(self, obj):
        cache_key = f"article_{obj.id}_average_score"
        average_score = cache.get(cache_key)
        if average_score is None:
            scores = obj.scores.all()
            if scores:
                average_score = sum([score.score for score in scores]) / len(scores)
            else:
                average_score = 0
            cache.set(cache_key, average_score, timeout=3600)  # Cache for 1 hour
        return average_score


class ArticleScoreSerializer(serializers.Serializer):
    score = serializers.IntegerField(min_value=0, max_value=5, required=True)

    def validate(self, data):
        article_id = self.context.get('article_id')
        user = self.context.get('user')

        if not Article.objects.filter(id=article_id).exists():
            raise serializers.ValidationError("Article not found.")

        article = Article.objects.get(id=article_id)
        data['article'] = article

        score, created = Score.objects.get_or_create(
            article=article, user=user, defaults={"score": 0}
        )
        cooldown_time = timedelta(minutes=5)

        if not created and now() - score.updated_at < cooldown_time:
            raise serializers.ValidationError("You can update your score after 5 minutes.")

        data['score_instance'] = score
        return data
