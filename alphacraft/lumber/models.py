from django.db import models
from django_extensions.db.models import TimeStampedModel


class Source(TimeStampedModel):
    name = models.CharField(max_length=100)
    address = models.TextField(null=True)

    def __str__(self) -> str:
        return self.name


class Log(TimeStampedModel):
    thickness = models.FloatField()
    width = models.FloatField()
    length = models.FloatField()
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True)

    @property
    def volume(self):
        return (self.thickness * self.width * self.width) / 12

    def __str__(self) -> str:
        return f"<{self.thickness}x{self.width}x{self.length} - {self.volume}"


class Lumber(TimeStampedModel):
    thickness = models.FloatField()
    width = models.FloatField()
    length = models.FloatField()
    log_source = models.ForeignKey(Log, on_delete=models.SET_NULL, null=True)
    # bought directly from source
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True)

    @property
    def volume(self):
        return (self.thickness * self.width * self.width) / 12

    def __str__(self) -> str:
        return f"<{self.thickness}x{self.width}x{self.length} - {self.volume}"
