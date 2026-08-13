from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from pydantic import ValidationError

from catalogue.loader import CatalogueError, load_catalogue


class Command(BaseCommand):
    help = "Validate all version-controlled card definitions and rule files."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--path",
            type=Path,
            default=settings.CARD_CATALOGUE_DIR,
            help="Catalogue cards directory to validate.",
        )

    def handle(self, *args, **options) -> None:
        path = options["path"]
        try:
            catalogue = load_catalogue(path, use_cache=False)
        except (CatalogueError, ValidationError, OSError) as exc:
            raise CommandError(str(exc)) from exc

        rule_count = sum(len(card.rules) for card in catalogue.cards)
        self.stdout.write(
            self.style.SUCCESS(
                f"Catalogue valid: {len(catalogue.cards)} card(s), "
                f"{rule_count} rule version(s)."
            )
        )
