from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class SearchInteraction(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    query = models.CharField(max_length=500)
    results_count = models.IntegerField()
    top_similarity = models.FloatField()
    model_used = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    processing_time = models.FloatField(help_text="Processing time in seconds")
    client_ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['user', '-created_at']),
        ]


class ImageInteraction(models.Model):
    search = models.ForeignKey(
        SearchInteraction,
        on_delete=models.CASCADE,
        related_name='image_interactions'
    )
    image_path = models.CharField(max_length=1000)
    similarity_score = models.FloatField()
    rank_position = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['search', 'rank_position']),
        ]
