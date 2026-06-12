from django.db import models
from django.conf import settings


class Song(models.Model):
    CATEGORY_CHOICES = [
        ('Entrance', 'Entrance'),
        ('Bible Procession', 'Bible Procession'),
        ('Offertory', 'Offertory'),
        ('Communion', 'Communion'),
        ('Thanksgiving', 'Thanksgiving'),
        ('Recessional', 'Recessional'),
        ('Responsorial Psalm', 'Responsorial Psalm'),
        ('ord-Kyrie', 'Ordinary — Kyrie'),
        ('ord-Gloria', 'Ordinary — Gloria'),
        ('ord-Sanctus', 'Ordinary — Sanctus'),
        ('ord-Agnus Dei', 'Ordinary — Agnus Dei'),
        ('ord-Other', 'Ordinary — Other'),
    ]

    LANGUAGE_CHOICES = [
        ('Swahili', 'Swahili'),
        ('Kikuyu', 'Kikuyu'),
        ('English', 'English'),
        ('Latin', 'Latin'),
        ('Other', 'Other'),
    ]

    MISA_CHOICES = [
        ('banana', 'Misa Banana'),
        ('subukia', 'Misa Subukia'),
        ('taita', 'Misa Taita'),
        ('amecea', 'Misa AMECEA'),
        ('other', 'Other Misa'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    language = models.CharField(max_length=50, choices=LANGUAGE_CHOICES)
    key_signature = models.CharField(max_length=20, blank=True)
    lyrics = models.TextField()
    misa_id = models.CharField(max_length=50, blank=True)
    ord_part = models.CharField(max_length=50, blank=True)
    has_score = models.BooleanField(default=False)
    score_file = models.FileField(upload_to='scores/', blank=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='songs',
    )
    uploaded_by_name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'title']

    def __str__(self) -> str:
        return self.title
