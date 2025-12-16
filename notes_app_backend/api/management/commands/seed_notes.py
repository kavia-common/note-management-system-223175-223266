from django.core.management.base import BaseCommand
from api.models import Note


class Command(BaseCommand):
    help = "Seeds the database with 5 sample notes."

    # PUBLIC_INTERFACE
    def handle(self, *args, **options):
        """Create sample notes if not already present."""
        samples = [
            {
                "title": "First Note",
                "content": "Welcome to the Notes app! This is your first note.",
                "tags": "welcome,getting-started",
                "archived": False,
            },
            {
                "title": "Grocery List",
                "content": "Milk, Eggs, Bread, Butter, Coffee",
                "tags": "personal,errands",
                "archived": False,
            },
            {
                "title": "Work Ideas",
                "content": "Investigate DRF filters, write design doc.",
                "tags": "work,ideas",
                "archived": False,
            },
            {
                "title": "Archived Sample",
                "content": "This note is archived.",
                "tags": "archive,example",
                "archived": True,
            },
            {
                "title": "Books to Read",
                "content": "Clean Code, Pragmatic Programmer, Deep Work",
                "tags": "personal,reading",
                "archived": False,
            },
        ]

        created = 0
        for s in samples:
            obj, was_created = Note.objects.get_or_create(
                title=s["title"],
                defaults={
                    "content": s["content"],
                    "tags": s["tags"],
                    "archived": s["archived"],
                },
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Seed complete. Created {created} new notes."))
