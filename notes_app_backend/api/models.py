from django.db import models


class Note(models.Model):
    """
    Note model representing a user note with title, content, optional tags,
    archive status, and timestamps.
    Tags are stored as a comma-separated string for simplicity.
    """
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, default="")
    tags = models.CharField(
        max_length=512,
        blank=True,
        default="",
        help_text="Comma-separated list of tags (e.g., work,personal,ideas)",
    )
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        ordering = ["-updated_at", "-created_at"]
        indexes = [
            models.Index(fields=["archived"]),
        ]

    def __str__(self) -> str:
        return f"{self.title} ({'archived' if self.archived else 'active'})"

    # PUBLIC_INTERFACE
    def tag_list(self):
        """Return tags as a list of strings (trimmed, non-empty)."""
        if not self.tags:
            return []
        return [t.strip() for t in self.tags.split(",") if t.strip()]
