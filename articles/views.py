from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from utils.anomaly_detection import detect_abnormal_activity, calculate_weighted_score
from utils.general import invalidate_cache
from .models import Article
from django.utils.timezone import now
from rest_framework import status

from .serializers import ArticleSerializer, ArticleScoreSerializer


class ArticleListView(APIView):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.all()
        response = []

        for article in articles:
            # Check for abnormal activity
            if detect_abnormal_activity(article.id):
                avg_score = "Under Review"  # Mark as suspicious
            else:
                avg_score = calculate_weighted_score(article.id)

            response.append({
                "title": article.title,
                "num_scores": article.scores.count(),
                "average_score": avg_score,
            })

        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the new article
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleScoreView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, version, pk):
        serializer = ArticleScoreSerializer(
            data=request.data,
            context={"article_id": pk, "user": request.user}
        )
        serializer.is_valid(raise_exception=True)

        score_instance = serializer.validated_data['score_instance']
        score_instance.score = serializer.validated_data['score']
        score_instance.updated_at = now()
        score_instance.save()

        # Invalidate cache for the article
        invalidate_cache(pk)

        return Response({"message": "Score updated successfully."})
