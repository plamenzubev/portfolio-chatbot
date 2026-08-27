from django.contrib import admin

from .models import Chunk, Document


class ChunkInline(admin.TabularInline):
    model = Chunk
    extra = 0
    readonly_fields = ("chunk_index", "text")
    fields = ("chunk_index", "text")
    can_delete = False


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "source_type", "updated_at")
    list_filter = ("source_type",)
    inlines = [ChunkInline]
