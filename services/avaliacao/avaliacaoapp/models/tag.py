import uuid
from django.db import models
from .timestamped import TimestampedModel

class Tag(TimestampedModel):
    _id = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4
    )
    tag = models.CharField(
        max_length=50
    )
    censurada = models.BooleanField(
        default=False
    )

    class Meta:
        db_table = 'tags'
        ordering = [
            'created'
        ]
