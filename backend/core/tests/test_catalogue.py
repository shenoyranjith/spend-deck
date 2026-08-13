from pathlib import Path

from django.test import SimpleTestCase

from catalogue.loader import load_catalogue


class CatalogueLoaderTests(SimpleTestCase):
    def test_example_catalogue_is_valid(self):
        repository_dir = Path(__file__).resolve().parents[3]
        cards_root = repository_dir / "catalog" / "examples"

        catalogue = load_catalogue(cards_root, use_cache=False)

        self.assertEqual(len(catalogue.cards), 1)
        loaded_card = catalogue.cards[0]
        self.assertEqual(loaded_card.card.id, "demo_card")
        self.assertEqual(loaded_card.rules[0].version, "2026-01-01")
