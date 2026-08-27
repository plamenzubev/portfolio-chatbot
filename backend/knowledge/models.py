from django.db import models


class Document(models.Model):
    """A single source of truth about you: a project, your CV, a blog post, etc."""

    class SourceType(models.TextChoices):
        PROJECT = "project", "Project"
        CV = "cv", "CV / resume"
        BLOG = "blog", "Blog post"
        BIO = "bio", "Bio / about"

    title = models.CharField(max_length=200)
    source_type = models.CharField(max_length=20, choices=SourceType.choices)
    content = models.TextField(help_text="Raw text this document is chunked and embedded from.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Chunk(models.Model):
    """A slice of a Document, embedded for similarity search."""

    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="chunks")
    chunk_index = models.PositiveIntegerField()
    text = models.TextField()
    embedding = models.JSONField(help_text="List[float] vector from the Ollama embedding model.")

    class Meta:
        ordering = ["document_id", "chunk_index"]

    def __str__(self):
        return f"{self.document.title} #{self.chunk_index}"
