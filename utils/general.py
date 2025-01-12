from django.core.cache import cache

def invalidate_cache(article_id):
    cache.delete(f"article_{article_id}_num_scores")
    cache.delete(f"article_{article_id}_average_score")