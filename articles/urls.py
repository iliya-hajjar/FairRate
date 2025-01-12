from django.urls import path
from .views import ArticleListView, ArticleScoreView

urlpatterns = [
    path('', ArticleListView.as_view(), name='article-list'),
    path('<int:pk>/score/', ArticleScoreView.as_view(), name='article-score'),
]
