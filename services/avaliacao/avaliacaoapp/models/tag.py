import uuid
from django.db import models

class Tag(models.Model):
    _id = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4
    )
    tag = models.CharField(
        max_length=50
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    censurada = models.BooleanField(
        default=False
    )

    class Meta:
        db_table = 'tags'
        ordering = [
            'created'
        ]
