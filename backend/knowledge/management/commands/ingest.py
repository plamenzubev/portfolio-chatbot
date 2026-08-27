import re
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction

from knowledge.models import Chunk, Document
from knowledge.ollama_client import embed

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"

# Each source file's name (without extension) is the source_type, e.g. data/project.md
CHUNK_MAX_CHARS = 800


def split_into_chunks(text: str, max_chars: int = CHUNK_MAX_CHARS) -> list[str]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks: list[str] = []
    current = ""
    for paragraph in paragraphs:
        if current and len(current) + len(paragraph) + 2 > max_chars:
            chunks.append(current)
            current = paragraph
        else:
            current = f"{current}\n\n{paragraph}" if current else paragraph
    if current:
        chunks.append(current)
    return chunks


class Command(BaseCommand):
    help = (
        "Re-builds the RAG knowledge base from markdown files in knowledge/data/. "
        "Each file is one Document; its filename stem must be a valid Document.SourceType "
        "and the first line (a '# Title' heading) becomes the Document title."
    )

    def handle(self, *args, **options):
        if not DATA_DIR.exists():
            self.stderr.write(f"No data directory at {DATA_DIR}")
            return

        for path in sorted(DATA_DIR.glob("*.md")):
            source_type = path.stem
            valid_types = {choice for choice, _ in Document.SourceType.choices}
            if source_type not in valid_types:
                self.stderr.write(
                    f"Skipping {path.name}: '{source_type}' is not one of {sorted(valid_types)}"
                )
                continue

            raw = path.read_text(encoding="utf-8")
            title_match = re.match(r"#\s*(.+)", raw)
            title = title_match.group(1).strip() if title_match else path.stem
            content = raw[title_match.end():].strip() if title_match else raw

            with transaction.atomic():
                document, _ = Document.objects.update_or_create(
                    title=title,
                    source_type=source_type,
                    defaults={"content": content},
                )
                document.chunks.all().delete()

                pieces = split_into_chunks(content)
                for index, piece in enumerate(pieces):
                    Chunk.objects.create(
                        document=document,
                        chunk_index=index,
                        text=piece,
                        embedding=embed(piece),
                    )

            self.stdout.write(self.style.SUCCESS(f"Ingested '{title}' ({len(pieces)} chunks)"))
