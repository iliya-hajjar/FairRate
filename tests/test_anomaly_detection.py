import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from articles.models import Article, Score
from django.contrib.auth.models import User
from utils.anomaly_detection import detect_abnormal_activity
from django.utils.timezone import now


@pytest.mark.django_db
class TestArticleListView:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)
        self.article1 = Article.objects.create(title="Article 1", content="Content 1")
        self.article2 = Article.objects.create(title="Article 2", content="Content 2")

        Score.objects.create(article=self.article1, user=self.user, score=5, updated_at=now())
        Score.objects.create(article=self.article2, user=self.user, score=3, updated_at=now())

    def test_get_articles(self):
        url = reverse('article-list', args=['v1'])
        response = self.client.get(url)

        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data[0]["title"] == self.article1.title
        assert response.data[0]["num_scores"] == 1
        assert round(response.data[0]['average_score'], 2) == 5

@pytest.mark.django_db
class TestArticleScoreView:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)
        self.article = Article.objects.create(title="Article 1", content="Content 1")

    def test_post_score(self):
        url = reverse('article-score', args=['v1', self.article.id])
        data = {"score": 4}

        response = self.client.post(url, data=data, format="json")
        assert response.status_code == 200
        assert response.data["message"] == "Score updated successfully."

        # Check if the score was saved
        score = Score.objects.get(article=self.article, user=self.user)
        assert score.score == 4

    def test_update_score_with_cooldown(self):
        url = reverse('article-score', args=['v1', self.article.id])
        data = {"score": 4}

        # First score
        self.client.post(url, data=data, format="json")

        # Try updating the score within cooldown
        data["score"] = 3
        response = self.client.post(url, data=data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "You can update your score after" in str(response.data)

    def test_score_invalid_article(self):
        url = reverse('article-score', args=['v1', 999])  # Invalid article ID
        data = {"score": 4}
        response = self.client.post(url, data=data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Article not found." in str(response.data)


@pytest.mark.django_db
class TestAbnormalDetectionScoreView:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)
        self.article = Article.objects.create(title="Article 1", content="Content 1")

    def test_detect_abnormal_activity(self):
        for _ in range(101):
            Score.objects.create(article=self.article, user=self.user, score=5, updated_at=now())

        assert detect_abnormal_activity(self.article.id) is True
