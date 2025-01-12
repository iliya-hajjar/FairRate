from datetime import timedelta
from django.utils.timezone import now

from articles.models import Score


def detect_abnormal_activity(article_id):
    """
    Detect whether there is abnormal activity for a specific article.
    """
    recent_scores = Score.objects.filter(
        article_id=article_id, updated_at__gte=now() - timedelta(minutes=10)
    )
    if recent_scores.count() > 100:  # Example threshold
        return True

    return False


def calculate_weighted_score(article_id):
    """
    Calculate the weighted average score for an article.
    Recent scores are weighted less to smooth abnormal activity.
    """
    scores = Score.objects.filter(article_id=article_id)
    total_weighted_score = 0
    total_weights = 0
    current_time = now()

    for score in scores:
        time_diff = (current_time - score.updated_at).total_seconds()
        weight = max(1, 3600 / (time_diff + 1))
        total_weighted_score += score.score * weight
        total_weights += weight

    return total_weighted_score / total_weights if total_weights > 0 else 0

