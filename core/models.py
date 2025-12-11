from django.db import models

class CorePillar(models.Model):
    title = models.CharField(max_length=120)
    summary = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Pillar"
        verbose_name_plural = "Pillars"

    def __str__(self):
        return self.title


class Service(models.Model):
    name = models.CharField(max_length=140)
    short_description = models.TextField(blank=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return self.name
